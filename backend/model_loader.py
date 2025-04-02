import os
from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
# Load environment variables
load_dotenv()

# Retrieve token
hf_token = os.getenv("HF_TRANSFORMERS_TOKEN")



# Dictionary to store multiple models
loaded_models = {}

def load_pipeline(model_name="mistralai/Mistral-7B-Instruct-v0.3"):
    """
    Loads a specified model with 4-bit quantization and returns a text-generation pipeline.
    If the model is already loaded, returns the cached instance.
    """
    if model_name in loaded_models:
        return loaded_models[model_name]  # Return already loaded model

    try:
        print(f"Loading model: {model_name} ...")
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            load_in_4bit=True,
            device_map="auto",
            use_auth_token=hf_token
        )
        
        tokenizer = AutoTokenizer.from_pretrained(model_name,use_auth_token=hf_token)

        loaded_models[model_name] = pipeline("text-generation", model=model, tokenizer=tokenizer)
        print(f"Model {model_name} loaded successfully.")

    except Exception as e:
        print(f"Error loading model {model_name}: {str(e)}")
        loaded_models[model_name] = None  # Prevent using a partially loaded model
        raise RuntimeError(f"Failed to load model {model_name}.") from e

    return loaded_models[model_name]

def unload_pipeline(model_name="mistralai/Mistral-7B-Instruct-v0.3"):
    """
    Unloads the specified model from memory and clears GPU cache.
    """
    print("trying to unload model:{} ".format(model_name))
    if model_name in loaded_models and loaded_models[model_name] is not None:
        try:
            print(f"Unloading model: {model_name} ...")
            del loaded_models[model_name]
            loaded_models[model_name] = None
            torch.cuda.empty_cache()  # Clear CUDA memory
            print(f"Model {model_name} unloaded successfully.")
        except Exception as e:
            print(f"Error unloading model {model_name}: {str(e)}")
            
    return None
