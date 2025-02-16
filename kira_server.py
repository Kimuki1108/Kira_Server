from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import os
import speech_recognition as sr
import numpy as np
import librosa
import pickle
import soundfile as sf
from gtts import gTTS

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Ovoz namunalari uchun model yuklash (agar mavjud bo‘lsa)
model_path = "voice_model.pkl"
if os.path.exists(model_path):
    with open(model_path, "rb") as f:
        voice_model = pickle.load(f)
else:
    voice_model = None


def extract_features(file_path):
    y, sr = librosa.load(file_path, sr=22050)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfccs, axis=1)


def verify_voice(file_path):
    if voice_model is None:
        return False
    features = extract_features(file_path)
    return voice_model.predict([features])[0] == 1


def speak(text):
    tts = gTTS(text=text, lang="uz")
    tts.save("output.mp3")
    os.system("mpg321 output.mp3")  # Serverda ovoz chiqmaydi


@app.route("/api", methods=["POST"])
def api():
    data = request.json
    if "text" not in data:
        return jsonify({"error": "No text provided"}), 400
    response = f"Sizning so‘rovingiz qabul qilindi: {data['text']}"
    return jsonify({"response": response})


@socketio.on("voice_command")
def handle_voice(data):
    audio_data = data.get("audio")
    if not audio_data:
        emit("response", {"error": "No audio received"})
        return
    
    with open("temp.wav", "wb") as f:
        f.write(audio_data)
    
    if verify_voice("temp.wav"):
        recognizer = sr.Recognizer()
        with sr.AudioFile("temp.wav") as source:
            audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio, language="uz-UZ")
            emit("response", {"text": text})
        except sr.UnknownValueError:
            emit("response", {"error": "Tushunarsiz ovoz"})
        except sr.RequestError:
            emit("response", {"error": "Ovoz tanish xizmati ishlamayapti"})
    else:
        emit("response", {"error": "Noto‘g‘ri foydalanuvchi ovozi"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port, debug=True)
