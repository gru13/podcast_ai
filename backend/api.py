from fastapi import FastAPI, UploadFile, File
import os
from backend.text_processing import preprocess_text, chunk_text
from backend.embedding_store import add_to_faiss, retrieve_top_chunks
from backend.refiner import refine_text

app = FastAPI()

# Upload a text file
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"temp/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    with open(file_location, "r", encoding="utf-8") as f:
        raw_text = f.read()

    print("Raw Text:", raw_text[:500])  # Print first 500 chars for debugging

    # Process text
    cleaned_text = preprocess_text(raw_text)
    print("Cleaned Text:", cleaned_text[:500])  # Debug cleaned text

    chunks = chunk_text(cleaned_text)
    print("Generated Chunks:", chunks)  # Debug chunk output

    # Store in FAISS
    add_to_faiss(chunks)

    return {"message": "File processed", "chunks": chunks}


@app.get("/retrieve/")
async def retrieve(query: str):
    print("User Query:", query)
    results = retrieve_top_chunks(query)  # Retrieve top chunks
    refined_output = refine_text(query, " ".join(results))  # Pass query + content
    print(results)
    print("\n\n\n\n\n")
    print(refined_output)
    return {"query": query, "refined_response": refined_output}

# Generate AI Discussion (Placeholder)
@app.get("/generate_discussion/")
async def generate_discussion():
    return {"discussion": ["Speaker 1: Hello!", "Speaker 2: Hi!"]}

# Convert to Speech (Placeholder)
@app.get("/generate_speech/")
async def generate_speech():
    return {"audio": "audio_file_path.mp3"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
