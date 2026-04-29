---
title: Research Agent
emoji: 🔍
colorFrom: blue
colorTo: indigo
sdk: docker
sdk_version: "3.0"
app_file: app.py
pinned: false
---

# 🔍 Multi-Source Research Agent

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Hugging%20Face-yellow)](https://huggingface.co/spaces/kumardatascience/research-agent)
[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-1.1.9-green)](https://langchain-ai.github.io/langgraph/)

An AI-powered research agent that automatically searches multiple web sources, reads full article content and generates structured professional reports with PDF export.

---

## 🚀 Live Demo

👉 **[Try it here](https://huggingface.co/spaces/kumardatascience/research-agent)**

---

## ✨ Features

- 🔍 **Multi-source research** — searches real websites via Tavily API
- 🤖 **Dual AI support** — Gemini 2.5 Flash + Groq Llama 3.3
- 📄 **PDF export** — download professional reports
- 🧠 **LangGraph agent** — smart research loop with 4 nodes
- 🌐 **Real internet data** — not from training data
- ⚡ **Always active** — never sleeps on Hugging Face

---

## 🏗️ How It Works

```
User enters topic
      ↓
Node 1: LLM generates 4 research questions
      ↓
Node 2: Tavily searches web (2 URLs per question)
      ↓
Node 3: BeautifulSoup scrapes page content
      ↓
Router: enough data? → loop back or continue
      ↓
Node 4: LLM synthesizes final report
      ↓
User downloads PDF
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| LangGraph 1.1.9 | Agent workflow engine |
| LangChain 1.2.15 | LLM toolkit |
| Gemini 2.5 Flash | Google AI model |
| Groq Llama 3.3 | Open source AI model |
| Tavily API | Web search |
| BeautifulSoup4 | HTML scraping |
| ReportLab | PDF generation |
| Streamlit | Web UI |

---

## 🚀 Run Locally

### 1. Clone the repo

```bash
git clone https://github.com/kumardatascience/research-agent.git
cd research-agent
```

### 2. Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -e .
```

### 4. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```
GEMINI_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
```

### 5. Run the app

```bash
streamlit run app.py
```

---

## 🔑 Getting API Keys

| API | Free Tier | Link |
|-----|-----------|------|
| Gemini | ✅ Free | [aistudio.google.com](https://aistudio.google.com) |
| Tavily | ✅ Free | [tavily.com](https://tavily.com) |
| Groq | ✅ Free | [console.groq.com](https://console.groq.com) |

---

## 📁 Project Structure

```
research-agent/
├── app.py                    # Streamlit UI
├── Dockerfile                # HF deployment
├── requirements.txt          # Dependencies
├── src/
│   └── research_agent/
│       ├── agent/
│       │   ├── graph.py      # LangGraph agent
│       │   └── tools.py      # Search + scrape tools
│       ├── report/
│       │   └── generator.py  # PDF generation
│       └── utils/
│           └── config.py     # Settings
└── docs/
    └── AGENT_FLOW.md         # Technical docs
```

---

## 👨‍💻 Author

Built by **Kumar Katariya**