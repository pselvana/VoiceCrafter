from faster_whisper import WhisperModel

model = WhisperModel("large-v3", device="cpu", compute_type="int8")
print("Downloaded model.")