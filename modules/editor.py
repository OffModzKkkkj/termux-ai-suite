import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

def create_assets(prompts):
    paths = []
    for i, prompt in enumerate(prompts):
        # Criando imagens com fundo estilizado e texto legível
        img = Image.new('RGB', (1280, 720), color=(10, 10, 10))
        d = ImageDraw.Draw(img)
        
        # Simular uma "imagem real" com formas geométricas e cores
        d.rectangle([0, 0, 1280, 720], fill=(20, 40, 60))
        d.ellipse([400, 100, 800, 500], fill=(100, 150, 200))
        
        try:
            font = ImageFont.truetype("/system/fonts/Roboto-Regular.ttf", 40)
        except:
            font = ImageFont.load_default()
            
        d.text((100, 600), prompt, font=font, fill=(255, 255, 255))
        path = f"assets/slide_{i}.png"
        img.save(path)
        paths.append(path)
    return paths

def assemble_video(image_paths, audio_path, output_path):
    # Efeito Ken Burns (Zoom/Movimento) e transições suaves
    # Este comando é mais complexo mas gera um vídeo muito melhor
    input_files = ""
    for img in image_paths:
        input_files += f"-loop 1 -t 5 -i {img} "
        
    cmd = (
        f"ffmpeg -y {input_files} -i {audio_path} "
        "-filter_complex \""
        "[0:v]zoompan=z='min(zoom+0.0015,1.5)':d=125:s=1280x720[v0]; "
        "[1:v]zoompan=z='min(zoom+0.0015,1.5)':d=125:s=1280x720[v1]; "
        "[2:v]zoompan=z='min(zoom+0.0015,1.5)':d=125:s=1280x720[v2]; "
        "[v0][v1][v2]concat=n=3:v=1:a=0[v]\" "
        "-map \"[v]\" -map 3:a -c:v libx264 -preset ultrafast -pix_fmt yuv420p "
        f"-c:a aac -shortest {output_path}"
    )
    
    subprocess.run(cmd, shell=True)
