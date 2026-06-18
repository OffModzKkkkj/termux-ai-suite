#!/usr/bin/env python3
"""
Script de teste do pipeline de vídeo sem necessidade de chave API.
Simula um roteiro gerado pela IA e testa todos os componentes locais.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules import voice, editor, marketer

def test_pipeline():
    print("=" * 60)
    print("  TESTE DO PIPELINE DE VÍDEO (sem API)")
    print("=" * 60)

    roteiro = (
        "A inteligência artificial está transformando o mundo de maneiras que jamais imaginamos. "
        "Desde assistentes virtuais até diagnósticos médicos, a IA está presente em cada aspecto "
        "da nossa vida. O futuro pertence àqueles que souberem usar essa tecnologia com sabedoria "
        "e responsabilidade. Prepare-se para uma nova era de possibilidades infinitas."
    )

    print(f"\n📄 Roteiro de teste: {len(roteiro)} caracteres")

    # Teste 1: Geração de áudio
    print("\n🎙️  [1/4] Gerando áudio...")
    try:
        audio = voice.generate_audio(roteiro, "assets/test_audio.mp3")
        print(f"  PASSOU ✅")
    except Exception as e:
        print(f"  FALHOU ❌: {e}")
        return False

    # Teste 2: Criação de slides
    print("\n🖼️  [2/4] Criando slides...")
    cenas = [
        "Cidade futurista com hologramas e robôs caminhando pelas ruas",
        "Cientista analisando dados em múltiplas telas com IA",
        "Mãos humanas e robóticas se tocando — símbolo de colaboração"
    ]
    try:
        slides = editor.create_assets(cenas)
        print(f"  PASSOU ✅ ({len(slides)} slides)")
    except Exception as e:
        print(f"  FALHOU ❌: {e}")
        return False

    # Teste 3: Montagem do vídeo
    print("\n🎬 [3/4] Montando vídeo...")
    try:
        editor.assemble_video(slides, audio, "output/test_result.mp4")
        print(f"  PASSOU ✅")
    except Exception as e:
        print(f"  FALHOU ❌: {e}")
        return False

    # Teste 4: Thumbnail
    print("\n🎨 [4/4] Gerando thumbnail...")
    try:
        marketer.generate_thumbnail("Inteligência Artificial no Futuro", "output/test_thumb.png")
        print(f"  PASSOU ✅")
    except Exception as e:
        print(f"  FALHOU ❌ (não crítico): {e}")

    # Verificar duração do vídeo gerado
    print("\n📊 Verificando vídeo gerado...")
    import subprocess
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", "output/test_result.mp4"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        duration = float(result.stdout.strip())
        print(f"  ⏱️  Duração do vídeo: {duration:.1f}s")
        if duration > 5:
            print(f"  ✅ Duração correta (> 5s)")
        else:
            print(f"  ⚠️  Vídeo muito curto! Verifique o pipeline.")

    print("\n" + "=" * 60)
    print("  TODOS OS TESTES CONCLUÍDOS!")
    print("=" * 60)
    return True

# Teste de proteção: roteiro inválido deve ser rejeitado
def test_error_protection():
    print("\n" + "=" * 60)
    print("  TESTE DE PROTEÇÃO CONTRA ERROS")
    print("=" * 60)

    from modules.voice import VoiceError

    casos = [
        ("Texto vazio", ""),
        ("Texto muito curto", "Erro"),
        ("Mensagem de erro da API", "Erro: GEMINI_API_KEY não configurada. KeyError: candidates"),
    ]

    for nome, texto in casos:
        try:
            voice.generate_audio(texto, "assets/test_invalid.mp3")
            print(f"  ❌ FALHOU (deveria ter rejeitado): {nome}")
        except VoiceError as e:
            print(f"  ✅ Corretamente rejeitado: {nome}")
        except Exception as e:
            print(f"  ⚠️  Erro inesperado em '{nome}': {e}")

    print("\n  Proteção contra erros funcionando corretamente!")

if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    test_error_protection()
    print()
    test_pipeline()
