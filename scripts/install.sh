#!/bin/bash

# Script de Instalação Inteligente - Termux AI Suite
# Otimizado para Redmi 13C 4G

# Pegar o diretório raiz do projeto
ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT_DIR"

echo "🚀 Iniciando instalação no diretório: $ROOT_DIR"

# 1. Atualizar e Instalar dependências do sistema
echo "📦 Instalando pacotes do sistema..."
pkg update && pkg upgrade -y
pkg install python ffmpeg git golang rust nodejs-lts -y

# 2. Instalar dependências Python
echo "🐍 Instalando dependências Python..."
pip install requests python-dotenv gTTS Pillow

# 3. Configurar e Compilar Go
echo "🐹 Compilando motor Go..."
if [ -f "engines/api_client.go" ]; then
    cd "$ROOT_DIR/engines"
    # Inicializa o módulo Go se não existir
    if [ ! -f "go.mod" ]; then
        go mod init termux-ai-suite/engines
    fi
    go build -o api_client api_client.go
    mv api_client "$ROOT_DIR/"
    cd "$ROOT_DIR"
else
    echo "⚠️ Aviso: engines/api_client.go não encontrado."
fi

# 4. Compilar Rust
echo "🦀 Compilando processador Rust..."
if [ -f "core/text_processor.rs" ]; then
    rustc core/text_processor.rs -o text_processor
else
    echo "⚠️ Aviso: core/text_processor.rs não encontrado."
fi

# 5. Configurar Node.js
echo "🟢 Configurando ambiente Node.js..."
if [ ! -f "package.json" ]; then
    npm init -y > /dev/null
    npm install dotenv > /dev/null
fi

echo ""
echo "✅ Instalação concluída com sucesso!"
echo "------------------------------------------------"
echo "Para começar:"
echo "1. Configure seu arquivo .env com as chaves API"
echo "2. Execute: python main.py --mode chat --prompt 'Olá'"
echo "------------------------------------------------"
