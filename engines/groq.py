import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Importar a mesma classe de erro para consistência
from engines.gemini import AIEngineError

def ask(prompt):
    """
    Envia um prompt para a API Groq e retorna o texto gerado.
    Lança AIEngineError com diagnóstico detalhado em caso de falha.
    """
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        raise AIEngineError(
            "GROQ_API_KEY não está configurada.\n"
            "  → Crie um arquivo .env na raiz do projeto com: GROQ_API_KEY=sua_chave\n"
            "  → Ou exporte no terminal: export GROQ_API_KEY=sua_chave\n"
            "  → Obtenha sua chave em: https://console.groq.com/"
        )

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 1024,
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
    except requests.exceptions.Timeout:
        raise AIEngineError("Tempo limite excedido ao conectar com a API Groq. Verifique sua conexão.")
    except requests.exceptions.ConnectionError as e:
        raise AIEngineError(f"Falha de conexão com a API Groq: {e}")

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
            400: "Requisição inválida. Verifique o modelo ou o formato do prompt.",
            401: "Chave de API inválida ou expirada. Gere uma nova em https://console.groq.com/",
            403: "Acesso negado. Verifique as permissões da sua chave.",
            429: "Limite de taxa (rate limit) excedido. Aguarde alguns segundos e tente novamente.",
            500: "Erro interno no servidor Groq. Tente novamente em alguns minutos.",
            503: "Serviço Groq temporariamente indisponível.",
        }.get(response.status_code, f"Erro HTTP {response.status_code}")

        raise AIEngineError(
            f"API Groq retornou erro {err_code}: {err_msg}\n"
            f"  → Diagnóstico: {diagnostico}"
        )

    # Extrair texto da resposta
    try:
        body = response.json()
        choices = body.get("choices", [])
        if not choices:
            raise AIEngineError(
                "A API Groq retornou uma resposta vazia (sem 'choices').\n"
                f"  → Resposta completa: {body}"
            )
        text = choices[0]["message"]["content"].strip()
        if not text:
            raise AIEngineError("A API Groq retornou um texto vazio.")
        return text
    except (KeyError, IndexError) as e:
        raise AIEngineError(
            f"Formato de resposta inesperado da API Groq: {e}\n"
            f"  → Resposta recebida: {response.text[:500]}"
        )
