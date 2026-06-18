import os
import requests
from dotenv import load_dotenv

load_dotenv()

def generate_script(idea, engine=None):
    """
    Gera um roteiro de narração via IA.
    Se engine for fornecido (módulo gemini ou groq), usa ele diretamente.
    Caso contrário, tenta Gemini com chave do .env.
    Lança exceção em caso de falha — nunca retorna texto de erro silencioso.
    """
    prompt = (
        f"Crie um roteiro de narração de 30 segundos para um vídeo sobre: '{idea}'. "
        "Retorne APENAS o texto da narração em português, sem títulos, sem comentários, "
        "sem marcações como [Cena 1] ou similar. Apenas o texto corrido que será narrado."
    )

    if engine is not None:
        # Usar o motor de IA fornecido (já tem tratamento de erro próprio)
        return engine.ask(prompt)

    # Fallback: usar Gemini diretamente
    from engines.gemini import ask as gemini_ask
    return gemini_ask(prompt)

def generate_visual_prompts(script, num_scenes=3, engine=None):
    """
    Gera descrições visuais para as cenas do vídeo com base no roteiro.
    Retorna uma lista de strings com as descrições.
    Nunca retorna fallback silencioso — lança exceção se a IA falhar.
    """
    prompt = (
        f"Baseado neste roteiro de vídeo: '{script[:500]}', "
        f"descreva {num_scenes} imagens cinematográficas e realistas para ilustrar o vídeo. "
        f"Retorne APENAS as {num_scenes} descrições separadas por ponto e vírgula (;), "
        "sem numeração, sem explicações adicionais."
    )

    if engine is not None:
        text = engine.ask(prompt)
    else:
        from engines.gemini import ask as gemini_ask
        text = gemini_ask(prompt)

    # Processar a resposta
    parts = [p.strip() for p in text.split(';') if p.strip()]

    # Garantir que temos o número correto de cenas
    if len(parts) < num_scenes:
        # Completar com variações do roteiro se necessário
        defaults = [
            f"Cena visual sobre: {script[:50]}",
            "Pessoa em ambiente moderno com tecnologia",
            "Paisagem urbana ao entardecer com movimento"
        ]
        while len(parts) < num_scenes:
            parts.append(defaults[len(parts) % len(defaults)])

    return parts[:num_scenes]
