from backend.model_loader import load_pipeline, unload_pipeline
from backend.text_processing import preprocess_text
import re

def refine_text(user_query, retrieved_chunks, model_pipeline):
    """Refines retrieved content into a smooth response based on user query."""
    
    MAX_INPUT_TOKENS = 3000  # Input limit
    MAX_NEW_TOKENS = 1000     # Output limit
    
    # Preprocess and concatenate retrieved chunks
    cleaned_content = preprocess_text(" ".join(retrieved_chunks))
    
    # Truncate input if needed
    truncated_content = cleaned_content[:MAX_INPUT_TOKENS]
    
    print("\n\n\nTruncated Content:", truncated_content[:500])  # Debug truncated content
    
    # Generate structured prompt
    prompt = f"""
    User asked: "{user_query}"
    
    Based on the retrieved content below, generate a structured and coherent answer:
    
    {truncated_content}

    Ensure the response is well-structured, logically connected, and directly answers the user's question.
    """

    # Generate output
    output = model_pipeline(prompt, max_new_tokens=MAX_NEW_TOKENS, do_sample=True, temperature=0.8)

    return output[0]["generated_text"].split("Ensure the response is well-structured, logically connected, and directly answers the user's question.")[-1]
