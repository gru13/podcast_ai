from transformers import pipeline

# Load a text-generation model (Example: Mistral-7B or Zephyr)
generator = pipeline("text-generation", model="mistralai/Mistral-7B")



def generate_discussion(refined_text):
    """
    Generate a structured podcast-style discussion from refined content.
    """
    prompt = f"""
    Generate a structured podcast discussion between two AI personas based on the following information:
    
    {refined_text}

    The conversation should be engaging, natural, and informative. Use a back-and-forth exchange with varied tones.
    
    Example:
    Speaker 1: Welcome to our discussion! Today, we’re diving into an exciting topic.
    Speaker 2: That’s right! Let's start by understanding the basics...

    Now, generate the conversation:
    """

    response = generator(prompt, max_length=500, num_return_sequences=1)
    dialogue = response[0]['generated_text'].split("\n")  # Split into speaker turns

    return dialogue
