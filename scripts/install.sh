#!/bin/bash

echo "🚀 Iniciando instalação ultraleve para Termux..."

# Atualizar pacotes
pkg update && pkg upgrade -y

# Instalar dependências básicas
pkg install python ffmpeg git golang rust nodejs-lts -y

# Criar ambiente virtual para economizar espaço e evitar conflitos (opcional, mas recomendado)
# Aqui instalaremos direto no sistema para simplificar no Redmi 13C
pip install requests python-dotenv gTTS Pillow

# Compilar utilitários de alta performance
echo "🦀 Compilando utilitários Rust e Go..."
rustc text_processor.rs -o text_processor
go build -o api_client api_client.go

echo "✅ Instalação poliglota concluída!"
echo "Use 'node index.js' para orquestração ou os binários ./api_client e ./text_processor diretamente."
