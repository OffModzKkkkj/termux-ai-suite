import os
import requests
from dotenv import load_dotenv

load_dotenv()

def ask(prompt):
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key: return "Erro: GEMINI_API_KEY não configurada."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, json=data)
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Erro Gemini: {e}"
