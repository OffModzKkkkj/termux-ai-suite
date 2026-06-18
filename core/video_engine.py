import os
import shutil
import subprocess
from engines import gemini, groq
from engines.gemini import AIEngineError
from modules import voice, editor, marketer, scripter
from modules.voice import VoiceError

def export_to_storage(source_path, filename):
    """Exporta o arquivo para o armazenamento do Android (apenas no Termux)."""
    target_dir = "/sdcard/Download/TermuxAI"
    try:
        if not os.path.exists(target_dir):
            subprocess.run(["mkdir", "-p", target_dir], check=False)

        target_path = os.path.join(target_dir, filename)
        shutil.copy(source_path, target_path)
        print(f"  📤 Exportado para o celular: {target_path}")
    except Exception as e:
        print(f"  ⚠️  Exportação para /sdcard ignorada (normal fora do Termux): {e}")

def create_video(idea, engine_name="gemini"):
    """
    Pipeline completo de criação de vídeo:
    1. Gera roteiro via IA
    2. Gera narração em áudio
    3. Cria slides visuais
    4. Monta o vídeo com duração correta
    5. Gera thumbnail
    6. Exporta para o celular (se no Termux)
    """
    print(f"\n🎬 Iniciando criação de vídeo | Motor: {engine_name.upper()} | Tema: {idea}")
    print("─" * 60)

    # Selecionar motor de IA
    engine = gemini if engine_name == "gemini" else groq

    # Garantir diretórios
    for folder in ["assets", "output"]:
        os.makedirs(folder, exist_ok=True)

    # ── ETAPA 1: Roteiro via IA ──────────────────────────────────────
    print("\n📝 [1/4] Gerando roteiro...")
    try:
        script = scripter.generate_script(idea, engine=engine)
        print(f"  ✅ Roteiro gerado ({len(script)} caracteres)")
        print(f"  📄 Prévia: {script[:120]}...")
    except AIEngineError as e:
        print(f"\n❌ FALHA NA GERAÇÃO DO ROTEIRO")
        print(f"{'─' * 60}")
        print(str(e))
        print(f"{'─' * 60}")
        print("⛔ Criação de vídeo cancelada. Corrija o erro acima e tente novamente.")
        return False
    except Exception as e:
        print(f"\n❌ Erro inesperado ao gerar roteiro: {e}")
        print("⛔ Criação de vídeo cancelada.")
        return False

    # ── ETAPA 2: Narração em áudio ───────────────────────────────────
    print("\n🎙️  [2/4] Gerando narração...")
    try:
        audio_path = voice.generate_audio(script, "assets/audio.mp3")
    except VoiceError as e:
        print(f"\n❌ FALHA NA GERAÇÃO DE ÁUDIO")
        print(f"{'─' * 60}")
        print(str(e))
        print(f"{'─' * 60}")
        print("⛔ Criação de vídeo cancelada.")
        return False
    except Exception as e:
        print(f"\n❌ Erro inesperado ao gerar áudio: {e}")
        print("⛔ Criação de vídeo cancelada.")
        return False

    # ── ETAPA 3: Slides visuais ──────────────────────────────────────
    print("\n🖼️  [3/4] Criando slides visuais...")
    try:
        # Gerar descrições de cenas via IA (com fallback gracioso)
        try:
            scene_prompts = scripter.generate_visual_prompts(script, num_scenes=3, engine=engine)
            print(f"  ✅ {len(scene_prompts)} cenas geradas pela IA")
        except (AIEngineError, Exception) as e:
            print(f"  ⚠️  IA não disponível para cenas visuais, usando descrições padrão: {e}")
            scene_prompts = [
                f"Introdução: {idea[:60]}",
                f"Desenvolvimento: aspectos principais sobre {idea[:40]}",
                f"Conclusão: reflexão final sobre {idea[:40]}"
            ]

        image_paths = editor.create_assets(scene_prompts)
    except Exception as e:
        print(f"\n❌ Erro ao criar slides: {e}")
        print("⛔ Criação de vídeo cancelada.")
        return False

    # ── ETAPA 4: Montagem do vídeo ───────────────────────────────────
    print("\n🎞️  [4/4] Montando vídeo final...")
    output_video = "output/result.mp4"
    try:
        editor.assemble_video(image_paths, audio_path, output_video)
    except Exception as e:
        print(f"\n❌ Erro ao montar vídeo: {e}")
        print("⛔ Criação de vídeo cancelada.")
        return False

    # ── THUMBNAIL ────────────────────────────────────────────────────
    print("\n🎨 Criando thumbnail...")
    try:
        marketer.generate_thumbnail(idea, "output/thumb.png")
        print("  ✅ Thumbnail criada: output/thumb.png")
    except Exception as e:
        print(f"  ⚠️  Thumbnail não gerada (não crítico): {e}")

    # ── EXPORTAR PARA CELULAR ────────────────────────────────────────
    print("\n📤 Exportando arquivos...")
    export_to_storage(output_video, f"video_{engine_name}.mp4")
    export_to_storage("output/thumb.png", f"thumb_{engine_name}.png")

    print("\n" + "═" * 60)
    print("✅ VÍDEO CRIADO COM SUCESSO!")
    print(f"   📹 Vídeo : {output_video}")
    print(f"   🖼️  Thumb : output/thumb.png")
    print("═" * 60)
    return True
