# termux-ai-suite 🚀🎬🦀

A **termux-ai-suite** é um ecossistema completo de inteligência artificial e criação de conteúdo projetado especificamente para rodar no Termux (Android), com otimizações especiais para dispositivos com recursos limitados (como o Redmi 13C 4G).

Esta suite unifica agentes de chat, motores de IA e um editor de vídeo agêntico em um único lugar, utilizando uma arquitetura poliglota para máxima performance.

## 🌟 Funcionalidades Unificadas

-   **Motores de IA (Engines)**: Integração direta com **Google Gemini** e **Groq** via REST API (ultraleve).
-   **Agente de Vídeo Agêntico**: Cria vídeos completos (roteiro, áudio, edição e thumbnail) usando os motores de IA integrados.
-   **Arquitetura Poliglota**:
    -   **Go**: Chamadas de API ultrarrápidas.
    -   **Rust**: Processamento de dados de alta performance.
    -   **Python**: Automação de mídia (gTTS, Pillow, FFmpeg).
    -   **Node.js**: Orquestração do sistema.

## 🛠️ Instalação

1.  **Clone a Suite**:
    ```bash
    git clone https://github.com/OffModzKkkkj/termux-ai-suite.git
    cd termux-ai-suite
    ```

2.  **Execute o instalador inteligente**:
    ```bash
    bash scripts/install.sh
    ```
    *Este script instalará Python, Node.js, Go, Rust e FFmpeg, além de compilar os binários de alta performance.*

3.  **Configure o ambiente**:
    Crie um arquivo `.env` na raiz:
    ```env
    GEMINI_API_KEY='sua_chave'
    GROQ_API_KEY='sua_chave'
    ```

## 🎥 Como Usar

A suite é controlada pelo script central `main.py`:

### Modo Chat (IA Pura)
```bash
python main.py --mode chat --engine groq --prompt "Como otimizar o Termux?"
```

### Modo Vídeo (Agente Editor)
```bash
python main.py --mode video --engine gemini --prompt "Explique o que é Rust em 30 segundos"
```

## 📂 Estrutura da Suite

-   `/engines`: Motores de conexão com APIs (Gemini, Groq, Go Client).
-   `/core`: Lógica central do editor de vídeo e processador Rust.
-   `/modules`: Utilitários de áudio, imagem e edição (FFmpeg).
-   `/scripts`: Scripts de instalação e manutenção.
-   `/output`: Onde seus vídeos e thumbnails finais são salvos.

## 🤝 Contribuição

Sinta-se à vontade para expandir esta suite com novos motores ou funcionalidades!

## 📄 Licença

MIT
