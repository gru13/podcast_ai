import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Initialize FAISS index
embedding_dim = embedding_model.get_sentence_embedding_dimension()
index = faiss.IndexFlatL2(embedding_dim)

# Store text chunks
chunk_store = []

def add_to_faiss(chunks):
    """Encodes and stores chunks in FAISS."""
    global chunk_store
    chunk_store.extend(chunks)  # Store original text
    
    # Convert text chunks to embeddings
    embeddings = embedding_model.encode(chunks)
    
    # Convert to NumPy array and store in FAISS
    embeddings = np.array(embeddings).astype('float32')
    index.add(embeddings)

def retrieve_top_chunks(query, top_k=25):
    """Retrieves the most relevant chunks based on a query."""
    query_embedding = embedding_model.encode([query]).astype('float32')
    distances, indices = index.search(query_embedding, top_k)

    results = [chunk_store[i] for i in indices[0] if i < len(chunk_store)]
    return results
