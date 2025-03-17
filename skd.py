# from TTS.api import TTS
# from playsound3 import playsound  # playsound3 provides the same import interface

# # Initialize the multi-speaker TTS model (VCTK/VITS)
# # tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=True, gpu=False)
# # Initialize the multi-speaker Tacotron2 model (VCTK)
# tts = TTS(model_name="tts_models/multilingual/multi-dataset/bark", progress_bar=True, gpu=False)

# # print(tts.speakers)# Select a speaker ID (change this number based on the available voices in the model)
# speaker_id = "p232" # male speaker
# # speaker_id = "p316" # female speaker

# # Define the text to synthesize
# text = "This is an example using a multi-speaker TTS model, and we are playing the audio using playsound3."

# # Specify the output file for the generated audio
# output_file = "multi_speaker_demo.wav"

# # Generate the speech and save to a file
# tts.tts_to_file(text=text, speaker=speaker_id, file_path=output_file)
# print(f"Multi-speaker audio saved to {output_file}")

# # Play the generated audio file using playsound3
# playsound(output_file)
# # # from TTS.api import TTS

# # # # This will print a dictionary of available models
# # # available_models = TTS.list_models()
# # # print(available_models)


# from transformers import AutoProcessor, BarkModel
# import torch
# import librosa
# import soundfile as sf
# from playsound3 import playsound  # or use playsound3 if needed

# # Initialize the processor and model
# processor = AutoProcessor.from_pretrained("suno/bark")
# model = BarkModel.from_pretrained("suno/bark")

# # Load and preprocess audio data
# audio_path = './sudeesh.wav'
# audio_input, sr = librosa.load(audio_path, sr=16000)  # Resample to 16kHz if necessary

# # Process the audio to the format the model expects
# inputs = processor(audio_input, sampling_rate=sr, return_tensors="pt")

# # Get the model's output (hidden states, logits, etc.)
# with torch.no_grad():
#     outputs = model(**inputs)

# # Extract the embeddings from the model (e.g., last hidden state)
# embeddings = outputs.last_hidden_state  # This contains the features of the audio

# # Optionally, you can pool or summarize the embeddings as needed for your application
# # For example, you might use mean pooling to get a fixed-size embedding vector
# speaker_embedding = embeddings.mean(dim=1)  # Pooling over time steps (sequence length)

# # Example: Generating speech with speaker embedding
# text_input = "Hello, how are you?"

# # Process the text input
# text_inputs = processor(text_input, return_tensors="pt")

# # Use speaker embedding to condition the model
# with torch.no_grad():
#     generated_speech = model.generate(input_ids=text_inputs['input_ids'], speaker_embeddings=speaker_embedding)

# # Save the generated speech as a .wav file
# output_path = 'generated_speech.wav'
# sf.write(output_path, generated_speech.cpu().numpy(), 16000)  # Save as WAV with a 16kHz sampling rate

# # Play the generated speech using playsound
# playsound(output_path)  # or use playsound3 if that's what you prefer


from playsound3 import playsound
playsound("./output_speech.wav")