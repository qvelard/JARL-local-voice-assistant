# JARLA Local Voice Assistant [WIP]

**JARLA** (Just A Realy Local Assistant) is a modular, extensible, LLM‑driven local voice assistant framework written in Python 3.11+. Designed to run entirely on your machine, JARL can listen, think, act, and speak without sending data to third‑party servers.


---

## Table of Contents

1. [Overview](#overview)
2. [Technical Stack & Choices](#technical-stack--choices)
3. [Architecture](#architecture)
4. [Project Structure](#project-structure)
5. [Installation](#installation)
6. [Configuration](#configuration)
7. [Usage](#usage)
8. [Testing](#testing)
9. [Contribution Guidelines](#contribution-guidelines)
10. [License](#license)

## Architecture Overview


- 🧠 **AI Agents**: autonomous agents (e.g. browser navigation, “smol” agents)  
- 🔧 **Core Modules**: audio I/O, STT/TTS, memory, plugin management, action dispatcher  
- 🔌 **Plugin System**: drop‑in “skills” under `core/skills/` that implement new intents  
- ⚙️ **Configurable Pipelines**: fully asynchronous (`asyncio`) orchestration, headless browser automation (Playwright), vector memory (ChromaDB)  
- 🧪 **Test Suite**: pytest coverage for unit & integration, JSON schema validation  

---

# Technical Stack & Choices

| Area                           | Component(s)                             | Rationale                                                                         |
| ------------------------------ | ---------------------------------------- | --------------------------------------------------------------------------------- |
| **Language**                   | Python 3.11+                             | Modern typing support, performance improvements, widespread library ecosystem.    |
| **Speech-to-Text (STT)**       | OpenAI Whisper, Vosk                     | Whisper for highest accuracy; Vosk as a lightweight alternative for edge devices. |
| **Text-to-Speech (TTS)**       | Coqui TTS, eSpeak                        | Coqui for natural voices; eSpeak for ultra-lightweight, phoneme‑level control.    |
| **Large Language Model (LLM)** | Ollama (local models) | Ollama enables hosting diverse LLMs locally for privacy, zero-latency access, and full control
| **Memory / Vector DB**         | ChromaDB                                 | Fast, simple vector store with Python API; supports semantic retrieval.           |
| **Browser Automation**         | Playwright, BeautifulSoup                | Playwright for headless browser control; BeautifulSoup for HTML parsing.          |
| **Configuration**              | YAML (`PyYAML`)                          | Human‑readable, supports comments, widely adopted.                                |
| **Plugin System**              | Python `importlib`, entry points         | Dynamic discovery and loading of new skills without modifying core code.          |
| **Testing**                    | `pytest`                                 | Simple, powerful testing framework with fixtures and plugins.                     |

## Architecture

flowchart LR
    subgraph Input Processing
      U["User (Voice Command)"] --> L[Listener]
      L --> S[Speech-to-Text]
    end
    subgraph Core Processing
      S --> O[Orchestrator]
      O --> M[Memory]
      O --> PM[Plugin Manager]
      O --> AD[Action Dispatcher]
      AD --> bash[System Commands]
      O --> BA[Browser Agent]
    end
    subgraph Output Generation
      O --> T[Text-to-Speech]
      T --> U2["User (Spoken Response)"]
    end

## Project Structure

```text
JARL-local-voice-assistant/
├── ai_agents/                  # Autonomous AI agents
│   └── browser_agent.py
│
├── core/                       # Core engine components
│   ├── listener.py            # Hotword/hotkey & audio capture
│   ├── stt.py                 # Local speech‑to‑text (Whisper/Vosk)
│   ├── tts.py                 # Local text‑to‑speech (Coqui‑TTS/eSpeak)
│   ├── memory.py              # Vector store (ChromaDB) & RAG
│   ├── action_dispatcher.py   # Map “plan steps” → system/browser actions
│   ├── plugin_manager.py      # Discover/load “skills” in core/skills/
│   └── utils.py               # Config loader, structured logger, JSON schema
│
├── core/skills/               # Custom “skill” modules (each implements can_handle/run)
│   └── example_skill.py
│
├── prompts/                    # LLM prompt templates & JSON schemas
│   ├── system_prompt.json
│   ├── user_prompt.tpl
│   └── cot_prompt.tpl
│
├── configs/                    # YAML configuration (hotkey, model names, etc.)
│   └── config.yaml
│
├── tests/                      # pytest unit & integration tests
│   ├── test_listener.py
│   ├── test_stt.py
│   ├── …  
│   └── test_utils.py
│
├── docker-compose.yml          # Orchestrator + ChromaDB + Redis (optional)
├── Dockerfile                  # GPU‑ready container image
├── main.py                     # Bootstrapper: hotkey loop → orchestrator → TTS
├── requirements.txt            # Pin exact dependencies
└── README.md                   # (You are reading it!)

## Installation

```bash
# Clone the repo
git clone https://github.com/qvelard/JARL-local-voice-assistant.git
cd JARL-local-voice-assistant

# (Optional) Create and activate a virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Copy the example config and edit:

```bash
cp configs/config.example.yaml configs/config.yaml
```

Key settings in `config.yaml`:

- `stt_engine`: `whisper` or `vosk`
- `tts_engine`: `coqui` or `espeak`
- `llm`: 
- `memory`: ChromaDB settings (embedding model, storage path)
- `hotword`: Custom activation keyword

## Usage

Run the main assistant:

```bash
python -m core.main --config configs/config.yaml
```

- Speak the hotword (default: “Hey JARL”)
- Give your command (“Open the browser and search Python tutorials.”)
- JARL will reply vocally and carry out the action.

## Testing

Execute the full test suite:

```bash
pytest --maxfail=1 --disable-warnings -q
```

## Contribution Guidelines

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-skill`)
3. Write tests for your feature
4. Follow the existing module patterns
5. Submit a pull request

Please ensure your code adheres to the [PEP8](https://peps.python.org/pep8/) style guide and includes type annotations.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

