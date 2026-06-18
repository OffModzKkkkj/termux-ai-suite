import os
from gtts import gTTS

# Comprimento mínimo de texto para considerar um roteiro válido (em caracteres)
MIN_SCRIPT_LENGTH = 30

class VoiceError(Exception):
    pass

def get_audio_duration(audio_path):
    """
    Retorna a duração em segundos de um arquivo de áudio usando ffprobe.
    Retorna None se não for possível determinar.
    """
    import subprocess
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                audio_path
            ],
            capture_output=True, text=True, timeout=10
        )
        duration = float(result.stdout.strip())
        return duration
    except Exception:
        return None

def generate_audio(text, output_path="assets/narration.mp3"):
    """
    Converte texto em áudio MP3 usando gTTS.
    Valida o texto antes de gerar para evitar narrar mensagens de erro.
    Retorna o caminho do arquivo gerado.
    Lança VoiceError se o texto for inválido ou a geração falhar.
    """
    # Validar se o texto existe e tem conteúdo suficiente
    if not text or not text.strip():
        raise VoiceError(
            "O roteiro está vazio. Não é possível gerar narração.\n"
            "  → Verifique se a API de IA retornou um roteiro válido."
        )

    text = text.strip()

    if len(text) < MIN_SCRIPT_LENGTH:
        raise VoiceError(
            f"O roteiro é muito curto ({len(text)} caracteres, mínimo: {MIN_SCRIPT_LENGTH}).\n"
            f"  → Texto recebido: \"{text}\"\n"
            "  → Isso pode indicar que a API retornou uma mensagem de erro em vez do roteiro."
        )

    # Detectar padrões de mensagem de erro comuns
    error_patterns = [
        "erro:", "error:", "api key", "api_key", "exception",
        "traceback", "keyerror", "indexerror", "não configurada",
        "invalid", "unauthorized", "forbidden", "rate limit"
    ]
    text_lower = text.lower()
    for pattern in error_patterns:
        if pattern in text_lower:
            raise VoiceError(
                f"O texto parece ser uma mensagem de erro, não um roteiro válido.\n"
                f"  → Padrão detectado: \"{pattern}\"\n"
                f"  → Texto recebido: \"{text[:200]}...\"\n"
                "  → Corrija o erro da API antes de gerar o vídeo."
            )

    # Garantir que o diretório de saída existe
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    try:
        tts = gTTS(text=text, lang='pt', slow=False)
        tts.save(output_path)
    except Exception as e:
        raise VoiceError(
            f"Falha ao gerar áudio com gTTS: {e}\n"
            "  → Verifique sua conexão com a internet (gTTS requer acesso ao Google)."
        )

    # Verificar se o arquivo foi criado e tem tamanho razoável
    if not os.path.exists(output_path):
        raise VoiceError("O arquivo de áudio não foi criado.")

    file_size = os.path.getsize(output_path)
    if file_size < 1000:  # menos de 1KB é suspeito
        raise VoiceError(
            f"O arquivo de áudio gerado é muito pequeno ({file_size} bytes).\n"
            "  → Possível falha silenciosa do gTTS."
        )

    # Informar duração do áudio gerado
    duration = get_audio_duration(output_path)
    if duration:
        print(f"  ✅ Áudio gerado: {output_path} ({duration:.1f}s)")
    else:
        print(f"  ✅ Áudio gerado: {output_path}")

    return output_path
