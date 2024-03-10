import whisper
import os
import numpy as np
import torch

torch.cuda.is_available()
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

model = whisper.load_model("base", device=DEVICE)

audio = whisper.load_audio("./audio.mp3")
audio = whisper.pad_or_trim(audio)
mel = whisper.log_mel_spectrogram(audio).to(model.device)

_, probs = model.detect_language(mel)
print(f"Detected language: {max(probs, key=probs.get)}")

options = whisper.DecodingOptions(language = 'en', without_timestamps=True, fp16 = False)
result = whisper.decode(model, mel, options)
print(result.text)

