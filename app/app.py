# app/app.py
from flask import Flask, render_template, request, jsonify
import whisper
import requests
import os
import json
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Initialize components
model = whisper.load_model("base")
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
PLAY_HT_API_KEY = os.getenv('PLAY_HT_API_KEY')

# Senior-focused configuration
SENIOR_PROFILE = {
    "preferred_voice": "male",
    "text_size": "large",
    "interaction_history": []
}

VOICES = {
    'male': 's3://voice-cloning-zero-shot/d9ff78ba-11d6-4b15-b60f-71cbc8014d3e/original/man1.mp3',
    'female': 's3://voice-cloning-zero-shot/2bc098a7-e136-4e2e-8c7e-0e0f5a62d9b3/original/woman1.mp3'
}

def save_interaction(user_input, response):
    interaction = {
        "timestamp": datetime.now().isoformat(),
        "input": user_input,
        "response": response,
        "keywords": ["medical" if "medicine" in user_input.lower() else "general"]
    }
    SENIOR_PROFILE["interaction_history"].append(interaction)
    
    # Save to JSON file (in real project use database)
    with open('user_profile.json', 'w') as f:
        json.dump(SENIOR_PROFILE, f)

@app.route('/')
def home():
    return render_template('index.html', voices=list(VOICES.keys()))

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    try:
        audio_file = request.files['audio']
        temp_path = f"temp_{datetime.now().timestamp()}.wav"
        audio_file.save(temp_path)
        
        result = model.transcribe(temp_path)
        os.remove(temp_path)
        
        return jsonify({'text': result["text"]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/synthesize', methods=['POST'])
def synthesize_speech():
    try:
        data = request.json
        headers = {
            'Authorization': f'Bearer {PLAY_HT_API_KEY}',
            'X-User-ID': 'public',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            'https://play.ht/api/v2/tts/instant',
            headers=headers,
            json={
                'text': data['text'],
                'voice': VOICES[data['voice']],
                'speed': 0.8  # Slower speed for clarity
            }
        )
        
        if response.status_code == 200:
            return jsonify({'audioUrl': response.json()['audioUrl']})
        return jsonify({'error': 'TTS failed'}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json['message']
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Senior-focused prompt engineering
        response = model.generate_content(
            f"""You are CARA - Caring Assistant for Retired Adults. Follow these rules:
            1. Use simple words and short sentences
            2. Speak slowly and clearly
            3. Always be positive and encouraging
            4. Ask clarifying questions if unsure
            5. Prioritize health/safety reminders
            
            Current interaction history: {SENIOR_PROFILE['interaction_history'][-3:]}
            
            User message: {user_message}"""
        )
        
        save_interaction(user_message, response.text)
        return jsonify({'text': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)