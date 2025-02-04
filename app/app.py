from flask import Flask, render_template, request, jsonify
import whisper
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
model = whisper.load_model("base")
PLAY_HT_API_KEY = os.getenv('PLAY_HT_API_KEY')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    print("\n[DEBUG] Received audio file")  # <-- NEW
    try:
        audio_file = request.files['audio']
        print(f"[DEBUG] Audio file: {audio_file.filename}")  # <-- NEW
        audio_path = f"temp_{audio_file.filename}"
        audio_file.save(audio_path)
        
        print("[DEBUG] Starting transcription...")  # <-- NEW
        result = model.transcribe(audio_path)
        print(f"[DEBUG] Transcription: {result['text']}")  # <-- NEW
        
        os.remove(audio_path)
        return jsonify({'text': result['text']})
    
    except Exception as e:
        print(f"[ERROR] Transcription failed: {str(e)}")  # <-- NEW
        return jsonify({'error': str(e)}), 500

@app.route('/synthesize', methods=['POST'])
def synthesize_speech():
    text = request.json['text']
    
    headers = {
        'Authorization': f'Bearer {PLAY_HT_API_KEY}',
        'X-User-ID': 'public'
    }
    
    data = {
        'text': text,
        'voice': 's3://voice-cloning-zero-shot/2bc098a7-e136-4e2e-8c7e-0e0f5a62d9b3/original/man1.mp3'
    }
    
    response = requests.post('https://play.ht/api/v2/tts/instant', headers=headers, json=data)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(port=5000, debug=True)