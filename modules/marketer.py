import os
from PIL import Image, ImageDraw, ImageFont

def generate_title(idea):
    # Gera um título clickbait profissional
    return f"O SEGREDO DO {idea.upper()}!"

def generate_thumbnail(title, output_path):
    # Criar uma thumbnail com gradiente e texto estilizado
    width, height = 1280, 720
    img = Image.new('RGB', (width, height), color=(20, 20, 20))
    d = ImageDraw.Draw(img)
    
    # Adicionar um gradiente simples (simulado)
    for i in range(height):
        r = int(255 * (i / height))
        d.line([(0, i), (width, i)], fill=(r, 0, 50))
    
    # Tentar carregar uma fonte, senão usa a padrão
    try:
        # No Termux as fontes ficam em caminhos específicos
        font = ImageFont.truetype("/system/fonts/Roboto-Bold.ttf", 80)
    except:
        font = ImageFont.load_default()
    
    # Adicionar contorno ao texto para destaque
    text_pos = (100, 300)
    d.text((text_pos[0]-5, text_pos[1]-5), title, font=font, fill=(0,0,0))
    d.text((text_pos[0]+5, text_pos[1]+5), title, font=font, fill=(0,0,0))
    d.text(text_pos, title, font=font, fill=(255, 255, 0)) # Amarelo vibrante
    
    img.save(output_path)
