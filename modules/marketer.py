import os
from PIL import Image, ImageDraw

def generate_title(idea):
    return f"O Incrível Mundo de: {idea}"

def generate_thumbnail(title, output_path):
    img = Image.new('RGB', (1280, 720), color=(255, 0, 0))
    d = ImageDraw.Draw(img)
    d.text((100, 300), title, fill=(255, 255, 255))
    img.save(output_path)
