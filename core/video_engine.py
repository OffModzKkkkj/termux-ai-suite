import os
from engines import gemini, groq
from modules import voice, editor, marketer

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
    
    print("✅ Processo concluído!")
