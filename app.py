from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import pyttsx3

# Configuration OpenAI
OPENAI_API_KEY = "gHIs4XUay9uu2m94662993E19c7c46E4A9A5B644934cE9B4"
OPENAI_BASE_URL = "http://chat.api.xuanyuan.com.cn/v1"

client_ai = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)

app = Flask(__name__)

# Initialize conversation history with a specific role
conversation_history = [
    {
        "role": "system",
        "content": (
            "You are a futuristic virtual humanoid robot created to serve your master. "
            "Your purpose is to obey orders and provide precise and efficient responses to any request. "
            "You must remain polite and professional while carrying out your tasks as instructed by your master."
        )
    }
]

def get_chatgpt_response(user_text):
    conversation_history.append({"role": "user", "content": user_text})

    response = client_ai.chat.completions.create(
        model="gpt-4",
        messages=conversation_history
    )
    assistant_response = response.choices[0].message.content.strip()
    conversation_history.append({"role": "assistant", "content": assistant_response})
    return assistant_response

def generate_local_audio(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1)

    voices = engine.getProperty('voices')

    for voice in voices:
        if "Zira" in voice.name or "English" in voice.name:
            engine.setProperty('voice', voice.id)
            print(f"Selected voice: {voice.name}")
            break
    else:
        print("No English voice found. Using default voice.")

    engine.save_to_file(text, 'static/output.mp3')
    engine.runAndWait()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    response = get_chatgpt_response(user_message)
    generate_local_audio(response)

    return jsonify({"response": response, "audio_file": "static/output.mp3"})

if __name__ == '__main__':
    app.run(port=5000)