import os
import requests
from dotenv import load_dotenv

load_dotenv()

def ask(prompt):
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key: return "Erro: GROQ_API_KEY não configurada."
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"model": "llama3-8b-8192", "messages": [{"role": "user", "content": prompt}]}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Erro Groq: {e}"
