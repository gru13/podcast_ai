import gradio as gr
import requests
import os
import logging
from datetime import datetime
import json

# Configurations
BASE_URL = "http://127.0.0.1:8000"  # FastAPI Backend URL
TEMP_DIR = "/tmp/podcast_ai_uploads"
LOG_FILE = "app.log"

# Ensure temp directory exists
os.makedirs(TEMP_DIR, exist_ok=True)

# Configure Logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def log_message(level, message):
    """Helper function to log messages."""
    if level == "info":
        logging.info(message)
    elif level == "error":
        logging.error(message)
    print(message)  # Also print to console

def upload_file(file):
    """Saves file temporarily and sends it to the backend."""
    if file is None:
        return {"error": "No file uploaded. Please select a file."}

    try:
        # Log file upload
        log_message("info", f"File uploaded: {file.name}")

        # Send file to backend
        with open(file.name, "rb") as f:
            response = requests.post(f"{BASE_URL}/upload/", files={"file": (file.name, f)})

        if response.status_code == 200:
            return response.json()
        else:
            error_msg = response.json().get("detail", "Unknown error")
            log_message("error", f"Upload failed: {error_msg}")
            return {"error": f"Upload failed: {error_msg}"}

    except requests.exceptions.RequestException as e:
        log_message("error", f"Failed to connect to server: {str(e)}")
        return {"error": f"Failed to connect to server: {str(e)}"}

    except Exception as e:
        log_message("error", f"Unexpected error in upload_file: {str(e)}")
        return {"error": f"Unexpected error: {str(e)}"}

def retrieve_text(query):
    """Retrieves relevant text chunks based on the query."""
    if not query.strip():
        return "Error: Query cannot be empty."

    try:
        response = requests.get(f"{BASE_URL}/retrieve/", params={"query": query})
        
        if response.status_code == 200:
            log_message("info", f"Retrieved text for query: {query}")
            return response.json().get("refined_response", "No response received.")
        else:
            error_msg = response.json().get("detail", "Unknown error")
            log_message("error", f"Retrieval failed: {error_msg}")
            return f"Retrieval failed: {error_msg}"
    
    except requests.exceptions.RequestException as e:
        log_message("error", f"Failed to connect to server: {str(e)}")
        return f"Failed to connect to server: {str(e)}"

    except Exception as e:
        log_message("error", f"Unexpected error in retrieve_text: {str(e)}")
        return f"Unexpected error: {str(e)}"

def generate_discussion(text):
    """Generates AI discussion from retrieved text."""
    if not text.strip():
        return "Error: Input text is empty."

    try:
        response = requests.get(f"{BASE_URL}/generate_discussion/", params={"refined_text": text})
        
        if response.status_code == 200:
            log_message("info", "AI discussion generated successfully.")
            generate_discussion_text=response.json().get('generated_discussion')
            generate_discussion_text = "\n".join([f"{speaker} : {message}" for speaker, message in generate_discussion_text])
            return generate_discussion_text
        else:
            error_msg = response.json().get("detail", "Unknown error")
            log_message("error", f"Discussion generation failed: {error_msg}")
            return f"Generation failed: {error_msg}"

    except requests.exceptions.RequestException as e:
        log_message("error", f"Failed to connect to server: {str(e)}")
        return f"Failed to connect to server: {str(e)}"

    except Exception as e:
        log_message("error", f"Unexpected error in generate_discussion: {str(e)}")
        return f"Unexpected error: {str(e)}"

def generate_speech(discussion):
    if not discussion.strip():
        return "Error: No discussion available."
    try:
        # Ensure discussion is in the correct format
        discussion_lines = discussion.split("\n")
        formatted_discussion = []
        for line in discussion_lines:
            if ": " in line:
                speaker, text = line.split(": ", 1)
                formatted_discussion.append([speaker.strip(), text.strip()])
        
        print("Formatted Discussion:", formatted_discussion)  # Debug formatted discussion
        
        response = requests.post(f"{BASE_URL}/generate_speech/", json={"discussion": formatted_discussion})
        print("Response Status Code:", response.status_code)  # Debug response status code
        print("Response Content:", response.content)  # Debug response content
        
        if response.status_code == 200:
            audio_file = response.json().get("file_path", "No audio generated.")
            log_message("info", "Speech generation completed successfully.")
            return audio_file
        else:
            error_msg = response.json().get("detail", "Unknown error")
            log_message("error", f"Speech generation failed: {error_msg}")
            return f"Speech generation failed: {error_msg}"
    except json.JSONDecodeError as e:
        log_message("error", f"JSON decode error: {str(e)}")
        return f"JSON decode error: {str(e)}"
    except requests.exceptions.RequestException as e:
        log_message("error", f"Failed to connect to server: {str(e)}")
        return f"Failed to connect to server: {str(e)}"
    except Exception as e:
        log_message("error", f"Unexpected error in generate_speech: {str(e)}")
        return f"Unexpected error: {str(e)}"


# Gradio Interface
with gr.Blocks() as app:
    gr.Markdown("# 🎙️ AI Podcast Generator")

    with gr.Row():
        file_input = gr.File(label="Upload Text File", type='filepath')
        upload_btn = gr.Button("Upload")

    upload_output = gr.JSON()
    upload_btn.click(upload_file, inputs=file_input, outputs=upload_output)

    query_input = gr.Textbox(label="Enter Search Query")
    retrieve_btn = gr.Button("Retrieve Chunks")
    retrieve_output = gr.Textbox(label="Refined Text Output")
    retrieve_btn.click(retrieve_text, inputs=query_input, outputs=retrieve_output)

    generate_btn = gr.Button("Generate Discussion")
    discussion_output = gr.Textbox(label="AI Discussion Output")
    generate_btn.click(generate_discussion, inputs=retrieve_output, outputs=discussion_output)

    speech_btn = gr.Button("Generate Speech")
    speech_output = gr.Audio(label="Generated Audio")
    speech_btn.click(generate_speech, inputs=discussion_output, outputs=speech_output)

# Run Gradio app    
app.launch(server_name="0.0.0.0", server_port=7860)