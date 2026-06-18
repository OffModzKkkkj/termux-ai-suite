#!/bin/bash

# Script de Instalação Inteligente - Termux AI Suite (V3)
# Otimizado para Redmi 13C 4G

# Pegar o diretório raiz do projeto
ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT_DIR"

echo "🚀 Iniciando instalação no diretório: $ROOT_DIR"

# VERIFICAÇÃO CRÍTICA: Impedir instalação em storage/shared (causa erros de Go/Rust)
if [[ "$ROOT_DIR" == *"/storage/shared"* ]]; then
    echo "❌ ERRO DETECTADO: Você está tentando instalar na memória compartilhada (/storage/shared)."
    echo "As linguagens Go e Rust não permitem compilação nesta pasta devido a restrições do Android."
    echo ""
    echo "💡 SOLUÇÃO: Mova o projeto para a memória interna do Termux com os comandos:"
    echo "   cd ~"
    echo "   mv $ROOT_DIR ."
    echo "   cd termux-ai-suite"
    echo "   bash scripts/install.sh"
    exit 1
fi

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
    # Tentar compilar sem travar arquivos (para maior compatibilidade)
    go build -o api_client api_client.go
    if [ -f "api_client" ]; then
        mv api_client "$ROOT_DIR/"
        echo "✅ Motor Go compilado."
    else
        echo "❌ Falha ao compilar Go."
    fi
    cd "$ROOT_DIR"
fi

# 4. Compilar Rust
echo "🦀 Compilando processador Rust..."
if [ -f "core/text_processor.rs" ]; then
    rustc core/text_processor.rs -o text_processor
    echo "✅ Processador Rust compilado."
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
