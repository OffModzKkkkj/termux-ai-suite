import os
import shutil
import subprocess
from engines import gemini, groq
from modules import voice, editor, marketer

def export_to_storage(source_path, filename):
    # Tentar exportar para a pasta de Downloads do Android
    target_dir = "/sdcard/Download/TermuxAI"
    try:
        if not os.path.exists(target_dir):
            subprocess.run(["mkdir", "-p", target_dir])
        
        target_path = os.path.join(target_dir, filename)
        shutil.copy(source_path, target_path)
        print(f"📤 Vídeo exportado para o celular: {target_path}")
    except Exception as e:
        print(f"⚠️ Não foi possível exportar para o armazenamento externo. Verifique as permissões (termux-setup-storage). Erro: {e}")

def create_video(idea, engine_name="gemini"):
    print(f"🎬 Iniciando criação de vídeo com o motor: {engine_name}")
    
    engine = gemini if engine_name == "gemini" else groq
    
    # 1. Roteiro via IA
    print("📝 Gerando roteiro...")
    script = engine.ask(f"Crie um roteiro de 30 segundos para um vídeo sobre: {idea}")
    
    # 2. Narração
    print("🎙️ Gerando áudio...")
    audio_path = voice.generate_audio(script, "assets/audio.mp3")
    
    # 3. Assets e Edição
    print("🎞️ Processando vídeo...")
    prompts = ["Intro", "Desenvolvimento", "Fim"]
    image_paths = editor.create_assets(prompts)
    editor.assemble_video(image_paths, audio_path, "output/result.mp4")
    
    # 4. Thumbnail
    print("🎨 Criando thumbnail...")
    marketer.generate_thumbnail(idea, "output/thumb.png")
    
    # Exportar para armazenamento do celular
    export_to_storage("output/result.mp4", f"video_{engine_name}.mp4")
    export_to_storage("output/thumb.png", f"thumb_{engine_name}.png")
    
    print("✅ Processo concluído!")
