import os
import requests

def generate_script(idea):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return f"Roteiro básico sobre: {idea}."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    prompt = (
        f"Crie um roteiro de 30 segundos sobre '{idea}'. "
        "Retorne APENAS o texto da narração, sem comentários."
    )
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return f"Roteiro para: {idea}"

def generate_visual_prompts(script):
    # Usa a IA para descrever 3 cenas visuais baseadas no roteiro
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return ["Cena 1", "Cena 2", "Cena 3"]
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    prompt = (
        f"Baseado neste roteiro: '{script}', descreva 3 imagens realistas e cinematográficas para ilustrar o vídeo. "
        "Retorne apenas as 3 descrições separadas por ponto e vírgula."
    )
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, json=data)
        text = response.json()['candidates'][0]['content']['parts'][0]['text']
        return [p.strip() for p in text.split(';') if p.strip()]
    except:
        return ["Fundo tecnológico azul", "Pessoa usando smartphone", "Futuro digital"]
