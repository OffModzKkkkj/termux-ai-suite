import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

# Paletas de cores para os slides (uma por slide, ciclando se houver mais)
SLIDE_PALETTES = [
    {"bg": (15, 25, 50),  "circle": (60, 120, 200), "text": (220, 240, 255)},
    {"bg": (20, 40, 20),  "circle": (60, 160, 80),  "text": (200, 255, 200)},
    {"bg": (50, 15, 30),  "circle": (200, 60, 100), "text": (255, 200, 220)},
    {"bg": (40, 30, 10),  "circle": (200, 160, 40), "text": (255, 240, 180)},
    {"bg": (20, 40, 50),  "circle": (40, 160, 200), "text": (180, 240, 255)},
]

def get_audio_duration(audio_path):
    """Retorna a duração em segundos do arquivo de áudio usando ffprobe."""
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
        return max(duration, 1.0)
    except Exception as e:
        print(f"  ⚠️ Não foi possível determinar duração do áudio: {e}. Usando 30s como padrão.")
        return 30.0

def wrap_text(text, max_chars_per_line=40):
    """Quebra texto longo em múltiplas linhas."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        if len(current) + len(word) + 1 <= max_chars_per_line:
            current = (current + " " + word).strip()
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return "\n".join(lines)

def create_assets(prompts):
    """
    Gera imagens PNG estilizadas para cada cena do vídeo.
    Retorna lista de caminhos dos arquivos gerados.
    """
    os.makedirs("assets", exist_ok=True)
    paths = []

    for i, prompt in enumerate(prompts):
        palette = SLIDE_PALETTES[i % len(SLIDE_PALETTES)]
        img = Image.new('RGB', (1280, 720), color=palette["bg"])
        d = ImageDraw.Draw(img)

        # Fundo com gradiente simulado
        for y in range(0, 720, 4):
            factor = int(30 * (1 - y / 720))
            r = min(255, palette["bg"][0] + factor)
            g = min(255, palette["bg"][1] + factor)
            b = min(255, palette["bg"][2] + factor)
            d.rectangle([0, y, 1280, y + 4], fill=(r, g, b))

        # Elemento decorativo
        d.ellipse([850, 50, 1250, 450], fill=palette["circle"])
        d.ellipse([910, 110, 1190, 390], fill=palette["bg"])

        # Carregar fontes
        try:
            font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
            font_main = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
        except Exception:
            try:
                font_big = ImageFont.truetype("/system/fonts/Roboto-Bold.ttf", 28)
                font_main = ImageFont.truetype("/system/fonts/Roboto-Regular.ttf", 36)
            except Exception:
                font_big = ImageFont.load_default()
                font_main = ImageFont.load_default()

        # Rótulo da cena
        d.text((60, 40), f"Cena {i + 1}", font=font_big, fill=(180, 180, 180))
        d.rectangle([60, 90, 800, 93], fill=palette["circle"])

        # Texto principal
        wrapped = wrap_text(prompt, max_chars_per_line=35)
        d.text((60, 120), wrapped, font=font_main, fill=palette["text"])

        path = f"assets/slide_{i}.png"
        img.save(path)
        paths.append(path)
        print(f"  🖼️  Slide {i + 1} criado: {path}")

    return paths

def assemble_video(image_paths, audio_path, output_path):
    """
    Monta o vídeo final combinando slides com fade suave e narração.
    Usa método leve (scale+fade) em vez de zoompan para melhor performance no Termux.
    A duração de cada slide é calculada com base na duração real do áudio.
    """
    os.makedirs(
        os.path.dirname(output_path) if os.path.dirname(output_path) else "output",
        exist_ok=True
    )

    # Calcular duração real do áudio
    audio_duration = get_audio_duration(audio_path)
    num_slides = len(image_paths)

    # Distribuir tempo entre slides com margem de segurança
    margin = 1.5
    slide_duration = (audio_duration + margin) / num_slides
    slide_duration = max(slide_duration, 3.0)

    fps = 25
    fade_duration = 0.5  # segundos de fade entre slides

    print(f"  ⏱️  Áudio: {audio_duration:.1f}s | Slides: {num_slides} | Duração/slide: {slide_duration:.1f}s")

    # ── Estratégia: gerar cada slide como clipe MP4 separado, depois concatenar ──
    clip_paths = []
    for i, img_path in enumerate(image_paths):
        clip_path = f"assets/clip_{i}.mp4"

        # Fade in no primeiro slide, fade out no último, ambos nos intermediários
        vf_parts = ["scale=1280:720:force_original_aspect_ratio=decrease",
                    "pad=1280:720:(ow-iw)/2:(oh-ih)/2"]

        if i == 0:
            vf_parts.append(f"fade=t=in:st=0:d={fade_duration}")
        if i == num_slides - 1:
            vf_parts.append(f"fade=t=out:st={slide_duration - fade_duration:.2f}:d={fade_duration}")

        vf = ",".join(vf_parts)

        cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", img_path,
            "-vf", vf,
            "-t", f"{slide_duration:.2f}",
            "-r", str(fps),
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-pix_fmt", "yuv420p",
            "-an",
            clip_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            raise RuntimeError(f"ffmpeg falhou ao criar clipe {i}: {result.stderr[-500:]}")

        clip_paths.append(clip_path)
        print(f"  🎞️  Clipe {i + 1}/{num_slides} processado")

    # ── Criar arquivo de lista para concatenação ──
    concat_list = "assets/concat_list.txt"
    with open(concat_list, "w") as f:
        for clip in clip_paths:
            f.write(f"file '{os.path.abspath(clip)}'\n")

    # ── Concatenar clipes e adicionar áudio ──
    print(f"  🔗 Concatenando clipes e adicionando narração...")
    cmd_final = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list,
        "-i", audio_path,
        "-map", "0:v",
        "-map", "1:a",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "128k",
        # Sem -shortest: o vídeo dura o tempo dos slides (já calculado com margem)
        output_path
    ]

    result = subprocess.run(cmd_final, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg falhou na concatenação: {result.stderr[-500:]}")

    # Limpar arquivos temporários
    for clip in clip_paths:
        try:
            os.remove(clip)
        except Exception:
            pass
    try:
        os.remove(concat_list)
    except Exception:
        pass

    if os.path.exists(output_path):
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"  ✅ Vídeo gerado: {output_path} ({size_mb:.1f} MB)")
    else:
        raise RuntimeError("O arquivo de vídeo não foi criado pelo ffmpeg.")
