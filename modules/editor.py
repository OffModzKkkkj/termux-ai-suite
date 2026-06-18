import os
import subprocess
from PIL import Image, ImageDraw

def create_assets(prompts):
    paths = []
    for i, prompt in enumerate(prompts):
        # Criando imagens menores para economizar RAM (720p -> 480p)
        img = Image.new('RGB', (854, 480), color=(30, 30, 30))
        d = ImageDraw.Draw(img)
        # Texto centralizado simples
        d.text((50, 200), prompt, fill=(255, 255, 255))
        path = f"assets/slide_{i}.png"
        img.save(path)
        paths.append(path)
    return paths

def assemble_video(image_paths, audio_path, output_path):
    # Usando configurações ultraleves do FFmpeg (ultrafast, resolução menor)
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", image_paths[0],
        "-i", audio_path,
        "-c:v", "libx264", "-preset", "ultrafast", "-t", "10", 
        "-vf", "scale=854:480", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k", "-shortest",
        output_path
    ]
    subprocess.run(cmd)
