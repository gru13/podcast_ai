from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from backend.text_processing import preprocess_text, chunk_text
from backend.embedding_store import add_to_faiss, retrieve_top_chunks, filter_relevant_chunks
from backend.refiner import refine_text
from backend.model_loader import load_pipeline, unload_pipeline
from backend.tts_generator import generate_ai_discussion
import os
import re

app = FastAPI()

# Ensure temp directory exists
if not os.path.exists("temp"):
    os.makedirs("temp")

# Load the model once when the API starts
model_pipeline = load_pipeline()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_location = f"temp/{file.filename}"

        # Save the uploaded file
        with open(file_location, "wb") as f:
            f.write(await file.read())

        # Read file contents
        with open(file_location, "r", encoding="utf-8") as f:
            raw_text = f.read()

        if not raw_text.strip():
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        print("Raw Text:", raw_text[:500])  # Debugging output

        # Process text
        cleaned_text = preprocess_text(raw_text)
        print("Cleaned Text:", cleaned_text[:500])  # Debug cleaned text

        # Chunk text
        chunks = chunk_text(cleaned_text)
        if not chunks:
            raise HTTPException(status_code=500, detail="Failed to generate text chunks.")

        print("Generated Chunks:", chunks[:5])  # Debug only first 5 chunks

        # Store in FAISS
        add_to_faiss(chunks)

        return {"message": "File processed successfully", "chunks": chunks}

    except Exception as e:
        print(f"Error in /upload/: {str(e)}")  # Log error
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.get("/retrieve/")
async def retrieve(query: str):
    print("User Query:", query)

    # Retrieve top chunks
    results = retrieve_top_chunks(query)

    if not results:
        return {"query": query, "refined_response": "No relevant content found."}

    # Filter relevant chunks
    filtered_chunks = filter_relevant_chunks(query, results)

    if not filtered_chunks:
        return {"query": query, "refined_response": "No highly relevant content found."}

    # Generate refined response
    refined_output = refine_text(query, " ".join(filtered_chunks), model_pipeline)

    # Unload model after inference to free memory
    unload_pipeline('mistralai/Mistral-7B-Instruct-v0.3')

    return {"query": query, "refined_response": refined_output}


# Generate AI Discussion (Placeholder)
@app.get("/generate_discussion/")
async def generate_discussion(refined_text: str):
    """
    Generates a conversation between two AI personas discussing the refined text.

    :param refined_text: The refined text extracted from retrieval.
    :return: A structured conversation as a list of tuples (speaker, content).
    """
    print("Generating AI Discussion...")

    # Conversation prompt
    prompt = f"""
    Generate a structured conversation between two AI personas (Person A and Person B) discussing the following topic:

    {refined_text}

    The conversation should be engaging, logical, and naturally flowing, where each persona questions or adds insights to the other's response.

    Format:
    Person A: [opening statement]  
    Person B: [response, follow-up question]  
    Person A: [answers, new insight]  
    Person B: [wrap-up or additional query]  
    """

    # Generate conversation
    output = model_pipeline(prompt, max_new_tokens=1000, do_sample=True, temperature=0.8)

    # Extract generated conversation
    raw_text = output[0]["generated_text"].split("Person B: [wrap-up or additional query]")[-1].strip()

    # Post-processing: Convert output into list of tuples
    conversation = []
    lines = raw_text.split("\n")

    for line in lines:
        match = re.match(r"^(Person [AB]):\s*(.*)", line.strip())  # Extract speaker and content
        if match:
            speaker, content = match.groups()
            conversation.append((speaker, content))

    return {"generated_discussion": conversation}


@app.post("/generate_speech/")
async def generate_speech(discussion: str = Form(...)):
    """
    Generates speech from an AI discussion where different speakers have different voices.
    
    :param discussion: A list of tuples where each tuple contains (speaker, text).
    :return: The generated .wav file.
    """
    output_path = "output_speech.wav"
    discussion = eval(discussion)
    print("Received Text:", discussion)
    # Generate speech using Coqui XTTS
    generate_ai_discussion(discussion, output_path)
    return {"message": "Speech generated successfully!", "file_path": output_path}

# @app.post("/generate_speech/")
# async def generate_speech(discussion: list):

#     # Return the generated file

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
