from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch
import os

# Load Hugging Face token from .env
hf_transformers_token = os.getenv('HF_TRANSFORMERS_TOKEN')

# Load Model with 4-bit quantization
model_name = "mistralai/Mistral-7B-Instruct-v0.3"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    load_in_4bit=True,  # Load in 4-bit to reduce VRAM usage
    torch_dtype=torch.float16,  # Use FP16 for better efficiency
    device_map="auto",  # Auto-assign to available GPU
    token=hf_transformers_token
)

tokenizer = AutoTokenizer.from_pretrained(model_name)

def refine_text(user_query, retrieved_chunks):
    """Refines retrieved content into a smooth response based on user query."""
    prompt = f"""
    User asked: "{user_query}"
    
    Based on the retrieved content below, generate a structured and coherent answer:
    
    {retrieved_chunks}

    Ensure the response is well-structured, logically connected, and directly answers the user's question.
    """

    # Tokenize input
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

    # Generate response
    with torch.no_grad():
        output = model.generate(**inputs, max_length=500, do_sample=True, temperature=0.7)

    # Decode output
    response = tokenizer.decode(output[0], skip_special_tokens=True)

    # Free up GPU memory
    del inputs, output
    torch.cuda.empty_cache()

    return response
