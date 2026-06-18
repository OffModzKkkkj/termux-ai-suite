import os
import argparse
from core import video_engine
from engines import gemini, groq

def main():
    print("====================================")
    print("      TERMUX AI SUITE (UNIFICADA)   ")
    print("====================================")
    
    # Garantir diretórios necessários
    for folder in ["assets", "output"]:
        if not os.path.exists(folder):
            os.makedirs(folder)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["chat", "video"], required=True)
    parser.add_argument("--engine", choices=["gemini", "groq"], default="gemini")
    parser.add_argument("--prompt", type=str)
    args = parser.parse_args()

    if args.mode == "chat":
        engine = gemini if args.engine == "gemini" else groq
        print(f"🤖 Chat ({args.engine}): {engine.ask(args.prompt)}")
        
    elif args.mode == "video":
        video_engine.create_video(args.prompt, args.engine)

if __name__ == "__main__":
    main()
