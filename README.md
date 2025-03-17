# Podcast AI Discussion System

## 📁 Project Structure
```
📁 podcast_ai/
│── 📁 backend/
│   ├── 📄 text_processing.py  # Preprocessing & Chunking
│   ├── 📄 embedding_store.py  # Embeddings & FAISS DB
│   ├── 📄 api.py              # FastAPI server to expose endpoints
│   ├── 📄 model_loader.py     # Model loading and unloading
│   ├── 📄 refiner.py          # Text refinement
│   ├── 📄 tts_generator.py    # Text-to-Speech (TTS) generation
│
│── 📁 frontend/
│   ├── 📄 app.py              # Gradio UI
│
│── 📁 temp/
│   ├── 📄 sample.txt          # Sample text file for testing
│
│── 📄 requirements.txt        # Dependencies
│── 📄 README.md               # Project Docs
│── 📄 .gitignore              # Git ignore file
```

## Project Overview

The Podcast AI Discussion System is designed to generate natural-sounding podcast-style discussions from text files. The system processes large text files, retrieves relevant content based on user queries, generates AI discussions, and converts them into speech.

### Key Components

1. **Text Processing & Chunking**
2. **Embedding & Context Retrieval**
3. **AI Discussion Generation**
4. **Text-to-Speech (TTS) Generation**
5. **User Interface & API Integration**

---

## 1️⃣ Text Processing & Chunking

### Goal
Efficiently process large text files into meaningful chunks for retrieval.

### Tech Used
- **BERTopic** for topic-based chunking
- **NLTK / SpaCy** for sentence & paragraph segmentation

### Process
1. **Load Text File**: Read raw text input.
2. **Preprocess**: Remove noise, standardize formatting.
3. **Semantic Chunking**:
   - Use **BERTopic** to detect topic shifts.
   - Dynamically adjust chunk size based on topic coherence.
   - Overlapping chunks ensure smooth transitions.

---

## 2️⃣ Embedding & Context Retrieval

### Goal
Retrieve the most relevant text chunks based on user queries.

### Tech Used
- **Sentence Transformers** for embedding generation
- **FAISS** for efficient similarity search

### Process
1. **Convert Question to Embedding**: Encode using the same model used for text chunks.
2. **Retrieve Top-k Chunks**: Search FAISS for the nearest vector matches.
3. **Relevance Filtering**:
   - **Re-rank based on cosine similarity**
   - **LLM-assisted verification**: Check if the retrieved content truly answers the question.

### Challenges & Solutions
✅ **Irrelevant Context Retrieval** → Use **LLM-based verification** and **cross-attention re-ranking**.
✅ **Retrieval Accuracy** → Fine-tune embeddings, optimize FAISS parameters.
✅ **Handling Ambiguous Queries** → Expand queries using paraphrasing techniques.

---

## 3️⃣ AI Discussion Generation

### Goal
Generate a natural-sounding two-person discussion from retrieved context.

### Tech Used
- **Mistral-7B-Instruct** for response generation
- **Prompt engineering** for role-based dialogue structuring
- **Speaker Style Adaptation** to add variation in responses

### Process
1. **Structure the Conversation**:
   - Assign **two distinct personas**.
   - Ensure one persona asks engaging follow-ups.
2. **Generate Dialogue**:
   - Use **LLM with a structured prompt** to produce back-and-forth discussion.
   - Ensure responses strictly adhere to retrieved context.
3. **Post-processing**:
   - Apply **text cleaning & formatting**.
   - Adjust speaker tags for clarity.

### Challenges & Solutions
✅ **Maintaining Topic Focus** → Restrict LLM generations using system instructions.
✅ **Avoiding Hallucinations** → Use **retrieval-augmented generation (RAG)** to keep responses factual.
✅ **Lack of Engagement** → Fine-tune model responses for conversational flow.

---

## 4️⃣ Text-to-Speech (TTS) Generation

### Goal
Convert generated text into realistic podcast-style speech.

### Tech Used
- **Coqui TTS** for voice cloning
- **VITS** for high-quality synthesis

### Process
1. **Assign Voices**: Each speaker gets a distinct synthetic voice.
2. **Generate Speech**:
   - Use **VITS** for high-quality prosody.
   - Convert output to waveform using **soundfile**.
3. **Apply Post-processing**:
   - Normalize audio.
   - Add minor background effects for realism.

### Challenges & Solutions
✅ **Voice Consistency** → Use **speaker embeddings** for each character.
✅ **Naturalness** → Use **prosody adjustments & duration modeling**.
✅ **Latency Issues** → Optimize synthesis speed with VITS.

---

## 5️⃣ User Interface & API Integration

### Goal
Provide a user-friendly way to input text files, ask questions, and get a generated podcast.

### Tech Used
- **FastAPI** for backend services
- **Gradio** for frontend UI
- **Docker** for deployment

### Process
1. **User Uploads Context (TXT File)**.
2. **Backend Processes the Text & Stores in FAISS**.
3. **User Asks a Question → Retrieves Relevant Chunks**.
4. **AI Generates the Discussion**.
5. **TTS Converts Discussion into Speech**.
6. **User Downloads the Podcast**.

### Challenges & Solutions
✅ **Scalability** → Use **containerization (Docker)** & **async processing**.
✅ **UI Responsiveness** → Optimize API calls with batching.
✅ **User Control Over Output** → Provide voice selection & output tuning options.

---

## 🔥 Final Thoughts & Doability

### Overall Feasibility: 90-95% ✅
- All components have **proven open-source solutions**.
- Main challenges are **maintaining coherence, retrieval accuracy, and synthesis quality**.
- With careful implementation of **BERTopic, FAISS, LLM filtering, and high-quality TTS models**, this system can be highly functional!

---

## 🚀 Project Setup

### Prerequisites
- Python 3.9 or higher
- Docker (for containerization)
- Git (for version control)

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/gru13/podcast_ai.git
   cd podcast_ai
   ```

2. **Create a Virtual Environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download SpaCy Model**:
   ```bash
   python3.10 -m spacy download en_core_web_sm
   ```

5. **Run the Backend**:
   ```bash
   uvicorn backend.api:app --reload
   ```

6. **Run the Frontend**:
   ```bash
   python frontend/app.py
   ```

7. **Using Docker**:
   - **Build the Docker Image**:
     ```bash
     docker build -t podcast_ai .
     ```
   - **Run the Docker Container**:
     ```bash
     docker run -p 8000:8000 podcast_ai
     ```

### Notes
- Ensure all environment variables are set correctly.
- Refer to individual module documentation for specific configurations.

---

