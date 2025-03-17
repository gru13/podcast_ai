# import os
# import numpy as np
# import torch
# import soundfile as sf  # Importing the soundfile module
# from TTS.api import TTS

# # Load VITS model
# tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=True, gpu=False)
# male_speaker = "p232"
# female_speaker = "p316"

# def generate_speech(text, speaker_id=male_speaker, output_file="output.wav"):
#     """
#     Generate speech using the selected speaker ID.
#     """
#     wav = tts.tts(text=text, speaker=speaker_id)
#     tts.tts_to_file(text=text, speaker=speaker_id, file_path=output_file)
#     return output_file

# def generate_ai_discussion(conversation, output_path="generated_discussion.wav"):
#     """
#     Generates AI discussion as speech with predefined speakers.
#     Generates separate temp audio files and then joins them.
#     :param conversation: List of tuples, e.g., [("Person A", "Hello"), ("Person B", "Hi there!")]
#     :param output_path: Path to save the final speech output
#     """
#     if not conversation:
#         raise ValueError("Conversation is empty.")
    
#     temp_files = []
    
#     for i, (speaker, text) in enumerate(conversation):
#         speaker_id = male_speaker if speaker == "Person A" else female_speaker
#         temp_file = f"temp_{i}.wav"
#         tts.tts_to_file(text=text, speaker=speaker_id, file_path=temp_file)
#         temp_files.append(temp_file)
    
#     # Combine all temp audio files
#     audio_segments = []
#     for temp_file in temp_files:
#         wav, samplerate = sf.read(temp_file)
#         audio_segments.append(wav)
#         os.remove(temp_file)  # Clean up temp files
    
#     final_audio = np.concatenate(audio_segments)
#     sf.write(output_path, final_audio, samplerate=24000)
    
#     return output_path
import os
import numpy as np
import torch
import soundfile as sf  # Importing the soundfile module
from TTS.api import TTS

# Load VITS model
tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=True, gpu=False)
male_speaker = "p232"
female_speaker = "p316"

def generate_speech(text, speaker_id=male_speaker, output_file="output.wav", speed=1.0):
    """
    Generate speech using the selected speaker ID with adjustable speed.
    """
    wav = tts.tts(text=text, speaker=speaker_id, speed=speed)
    tts.tts_to_file(text=text, speaker=speaker_id, speed=speed, file_path=output_file)
    return output_file

def generate_ai_discussion(conversation, output_path="generated_discussion.wav"):
    """
    Generates AI discussion as speech with predefined speakers.
    Generates separate temp audio files and then joins them.
    :param conversation: List of tuples, e.g., [("Person A", "Hello"), ("Person B", "Hi there!")]
    :param output_path: Path to save the final speech output
    """
    if not conversation:
        raise ValueError("Conversation is empty.")
    
    temp_files = []
    
    for i, (speaker, text) in enumerate(conversation):
        speaker_id = male_speaker if speaker == "Person A" else female_speaker
        speed = 0.8 if speaker == "Person A" else 1.0  # Slow down male speaker slightly
        temp_file = f"temp_{i}.wav"
        tts.tts_to_file(text=text, speaker=speaker_id, speed=speed, file_path=temp_file)
        temp_files.append(temp_file)
    
    # Combine all temp audio files
    audio_segments = []
    for temp_file in temp_files:
        wav, samplerate = sf.read(temp_file)
        audio_segments.append(wav)
        os.remove(temp_file)  # Clean up temp files
    
    final_audio = np.concatenate(audio_segments)
    sf.write(output_path, final_audio, samplerate=24000)
    
    return output_path
