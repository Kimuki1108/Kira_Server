from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import pyttsx3
import webbrowser
import datetime
import random

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

jokes = [
    "Nega kompyuter shifoxonaga tushdi? Chunki virus yuqtirib qoldi!",
    "Hacker kimgadir telefon qilibdi: 'Parolni ayting, yoki o'zim topib olaman!'",
    "Ertaga hamma narsa yaxshi bo'ladi, lekin bugun ham shunchaki zavqlaning!"
]

motivations = [
    "Hech qachon taslim bo‘lmang! Eng zo‘r yutuqlarga yo‘l davomida duch kelasiz.",
    "Bugun bir qadam tashla, ertaga ikki qadam! Sen muvaffaqiyatga erishasan!",
    "Siz har doim eng yaxshi natijalarga loyiqsiz!"
]

@app.route('/')
def home():
    return "Kira AI Server ishlayapti!"

@socketio.on('message')
def handle_message(message):
    command = message.lower()
    response = ""

    if "youtube" in command:
        webbrowser.open("https://youtube.com")
        response = "YouTube ochildi"
    elif "google" in command:
        webbrowser.open("https://google.com")
        response = "Google ochildi"
    elif "kawaii.uz" in command:
        webbrowser.open("https://kawaii.uz")
        response = "Kawaii.uz ochildi"
    elif "vaqt nechchi" in command:
        now = datetime.datetime.now()
        response = f"Hozirgi vaqt {now.strftime('%H:%M')}"
    elif "sana nechchi" in command:
        now = datetime.datetime.now()
        response = f"Bugungi sana {now.strftime('%Y-%m-%d')}"
    elif "men xafaman" in command:
        response = random.choice(jokes + motivations)
    elif "dunyoda kim eng zo'ri" in command:
        response = "Kuragami Kyotaka"
    elif "sen kimga bo'ysinasan" in command:
        response = "Faqat sizga"
    elif "youtube ga video qo'ymoqchiman" in command:
        webbrowser.open("https://studio.youtube.com")
        response = "YouTube Studio ochildi"
    elif "youtube ga post" in command:
        webbrowser.open("https://www.youtube.com/channel/UC/community")
        response = "YouTube Community ochildi"
    elif "hayr" in command or "chiqish" in command:
        response = "Xayr, siz bilan ishlash maroqli bo'ldi!"
    else:
        response = "Kechirasiz, bu buyruqni tushunmadim."
    
    speak(response)
    emit('response', response)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
