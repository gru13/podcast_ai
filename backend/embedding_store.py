import faiss
import numpy as np
from sentence_transformers import SentenceTransformer, util

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



def filter_relevant_chunks(query: str, retrieved_chunks: list, threshold: float = 0.5) -> list:
    """
    Filters retrieved chunks based on semantic similarity to the query using SBERT.
    
    :param query: User's search query
    :param retrieved_chunks: List of retrieved text chunks
    :param threshold: Minimum cosine similarity score to keep a chunk
    :return: List of filtered relevant chunks
    """
    if not retrieved_chunks:
        return []

    # Compute embeddings for the query and chunks
    query_embedding = embedding_model.encode(query, convert_to_tensor=True)
    chunk_embeddings = embedding_model.encode(retrieved_chunks, convert_to_tensor=True)

    # Compute cosine similarity between query and each chunk
    similarities = util.pytorch_cos_sim(query_embedding, chunk_embeddings).squeeze(0)

    # Filter chunks based on similarity threshold
    filtered_chunks = [chunk for chunk, score in zip(retrieved_chunks, similarities) if score >= threshold]

    return filtered_chunks
