import os
import sys
import argparse
from core import video_engine
from engines import gemini, groq
from engines.gemini import AIEngineError

def main():
    print("╔══════════════════════════════════════════╗")
    print("║       TERMUX AI SUITE  —  v2.0           ║")
    print("║  Motor: Gemini / Groq  |  Vídeo + Chat   ║")
    print("╚══════════════════════════════════════════╝\n")

    # Garantir diretórios necessários
    for folder in ["assets", "output"]:
        os.makedirs(folder, exist_ok=True)

    parser = argparse.ArgumentParser(
        description="Termux AI Suite — Criação de vídeos e chat com IA",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--mode",
        choices=["chat", "video"],
        required=True,
        help="Modo de operação:\n  chat  → conversa com a IA\n  video → cria um vídeo completo"
    )
    parser.add_argument(
        "--engine",
        choices=["gemini", "groq"],
        default="gemini",
        help="Motor de IA a usar (padrão: gemini)"
    )
    parser.add_argument(
        "--prompt",
        type=str,
        required=True,
        help="Texto do prompt ou tema do vídeo"
    )
    args = parser.parse_args()

    if args.mode == "chat":
        engine = gemini if args.engine == "gemini" else groq
        print(f"🤖 Chat [{args.engine.upper()}]: enviando prompt...")
        try:
            resposta = engine.ask(args.prompt)
            print(f"\n💬 Resposta:\n{'─' * 50}\n{resposta}\n{'─' * 50}")
        except AIEngineError as e:
            print(f"\n❌ Falha na API de IA:\n{'─' * 50}\n{e}\n{'─' * 50}")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
            sys.exit(1)

    elif args.mode == "video":
        sucesso = video_engine.create_video(args.prompt, args.engine)
        if not sucesso:
            sys.exit(1)

if __name__ == "__main__":
    main()
