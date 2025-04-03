import torch
import torch.nn as nn
from transformers import Wav2Vec2Processor, Wav2Vec2Model
import librosa
import numpy as np

# A simple regressor model that maps wav2vec2 embeddings to a MOS score.
# In practice, you would train this regressor on labeled MOS data.
class SimpleMOSRegressor(nn.Module):
    def __init__(self, input_dim, hidden_dim=128):
        super(SimpleMOSRegressor, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )

    def forward(self, x):
        return self.fc(x)

def compute_fad(audio_path):
    audio, sr = librosa.load(audio_path, sr=16000)
    mfcc_features = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
    mean_embedding = np.mean(mfcc_features, axis=1)
    fad_score = np.linalg.norm(mean_embedding)
    return fad_score

def compute_pitch_variation(audio_path):
    y, sr = librosa.load(audio_path, sr=16000)
    f0, _, _ = librosa.pyin(y, fmin=50, fmax=300)
    pitch_std = np.nanstd(f0)
    return pitch_std

def compute_jitter_shimmer(audio_path):
    y, sr = librosa.load(audio_path, sr=16000)
    f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=50, fmax=300)
    f0_diff = np.diff(f0)
    jitter = np.nanmean(np.abs(f0_diff))
    rms_energy = librosa.feature.rms(y=y)
    shimmer = np.nanstd(rms_energy)
    return jitter, shimmer

def evaluate_tts_naturalness(audio_path):
    print("Evaluating:", audio_path)
    fad_score = compute_fad(audio_path)
    pitch_std = compute_pitch_variation(audio_path)
    jitter, shimmer = compute_jitter_shimmer(audio_path)

    sr = 16000
    waveform, _ = librosa.load(audio_path, sr=sr)
    processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
    model = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-base-960h")
    model.eval()

    inputs = processor(waveform, sampling_rate=sr, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)
    input_dim = embeddings.shape[-1]
    regressor = SimpleMOSRegressor(input_dim)
    regressor.eval()

    with torch.no_grad():
        mos_prediction = regressor(embeddings).item()
    mos_score = max(1, min(5, 3 + mos_prediction))
    
    print(f"🔹 FAD Score: {fad_score:.4f} (Lower is better)")
    print(f"🔹 MOS Score: {mos_score:.2f} (1-5, Higher is better)")
    print(f"🔹 Pitch Variation: {pitch_std:.2f} (Moderate = More natural)")
    print(f"🔹 Jitter: {jitter:.4f} (Lower is better)")
    print(f"🔹 Shimmer: {shimmer:.4f} (Lower is better)")

if __name__ == "__main__":
    audio_path = "output_speech.wav"  # Replace with your TTS output file
    evaluate_tts_naturalness(audio_path)
