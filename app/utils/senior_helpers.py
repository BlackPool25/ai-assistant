import whisper
import google.generativeai as genai
import os

class SeniorAssistant:
    def __init__(self):
        self.whisper_model = whisper.load_model("base")
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        self.gemini = genai.GenerativeModel('gemini-1.5-flash')
    
    def generate_response(self, text, user):
        prompt = f"""Act as a family member for {user.username} (senior citizen). Follow these rules:
        1. Use simple, warm language
        2. Keep responses under 3 sentences
        3. Ask follow-up questions
        4. Detect medical/important info
        5. Always be positive
        
        Message: {text}"""
        
        response = self.gemini.generate_content(prompt)
        return response.text
    
    def check_importance(self, text):
        important_keywords = ['medicine', 'doctor', 'hospital', 'pain', 'emergency']
        return any(keyword in text.lower() for keyword in important_keywords)