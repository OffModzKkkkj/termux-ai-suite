import os
import requests

def generate_script(idea):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return f"Roteiro básico sobre: {idea}. (Configure a API para roteiros melhores)"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{"text": f"Crie um roteiro curto de 1 minuto para um vídeo sobre: {idea}. O roteiro deve ser narrado por uma voz amigável."}]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    except:
        return f"Roteiro gerado para: {idea}"

def generate_visual_prompts(script):
    return ["Introdução", "Desenvolvimento", "Conclusão"]
