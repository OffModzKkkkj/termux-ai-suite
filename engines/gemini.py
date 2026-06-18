import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Classe de erro específica para falhas de API
class AIEngineError(Exception):
    pass

def ask(prompt):
    """
    Envia um prompt para a API Gemini e retorna o texto gerado.
    Lança AIEngineError com diagnóstico detalhado em caso de falha.
    """
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise AIEngineError(
            "GEMINI_API_KEY não está configurada.\n"
            "  → Crie um arquivo .env na raiz do projeto com: GEMINI_API_KEY=sua_chave\n"
            "  → Ou exporte no terminal: export GEMINI_API_KEY=sua_chave"
        )

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/gemini-1.5-flash:generateContent?key={api_key}"
    )
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, json=data, timeout=30)
    except requests.exceptions.Timeout:
        raise AIEngineError("Tempo limite excedido ao conectar com a API Gemini. Verifique sua conexão.")
    except requests.exceptions.ConnectionError as e:
        raise AIEngineError(f"Falha de conexão com a API Gemini: {e}")

    # Diagnóstico de erros HTTP
    if response.status_code != 200:
        try:
            err_body = response.json()
            err_msg = err_body.get("error", {}).get("message", response.text)
            err_code = err_body.get("error", {}).get("code", response.status_code)
        except Exception:
            err_msg = response.text
            err_code = response.status_code

        diagnostico = {
            400: "Requisição inválida. Verifique o formato do prompt.",
            401: "Chave de API inválida ou expirada. Gere uma nova em https://aistudio.google.com/",
            403: "Acesso negado. A chave pode não ter permissão para este modelo.",
            429: "Cota de uso excedida. Aguarde ou verifique seu plano em https://aistudio.google.com/",
            500: "Erro interno no servidor do Google. Tente novamente em alguns minutos.",
            503: "Serviço Gemini temporariamente indisponível. Tente novamente.",
        }.get(response.status_code, f"Erro HTTP {response.status_code}")

        raise AIEngineError(
            f"API Gemini retornou erro {err_code}: {err_msg}\n"
            f"  → Diagnóstico: {diagnostico}"
        )

    # Verificar bloqueio por segurança (promptFeedback)
    body = response.json()
    if "promptFeedback" in body:
        block_reason = body["promptFeedback"].get("blockReason", "")
        if block_reason:
            raise AIEngineError(
                f"Conteúdo bloqueado pela política de segurança do Gemini.\n"
                f"  → Motivo: {block_reason}\n"
                f"  → Reformule o prompt para evitar conteúdo sensível."
            )

    # Extrair texto da resposta
    try:
        candidates = body.get("candidates", [])
        if not candidates:
            raise AIEngineError(
                "A API Gemini retornou uma resposta vazia (sem 'candidates').\n"
                f"  → Resposta completa: {body}"
            )
        text = candidates[0]["content"]["parts"][0]["text"].strip()
        if not text:
            raise AIEngineError("A API Gemini retornou um texto vazio.")
        return text
    except (KeyError, IndexError) as e:
        raise AIEngineError(
            f"Formato de resposta inesperado da API Gemini: {e}\n"
            f"  → Resposta recebida: {body}"
        )
