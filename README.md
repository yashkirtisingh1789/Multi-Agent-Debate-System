# Multi-Agent Debate System

A multi-agent debate system built with **LangGraph**, **LangChain OpenAI**, and **Python** where autonomous AI personas (Optimist vs. Pessimist) argue a topic until an AI Judge declares a winner.

## Overview

The system features three distinct agents operating in a state graph workflow:
- **Optimist Agent**: Argues the positive perspective on a given topic.
- **Pessimist Agent**: Counters the arguments with critical points and flaws.
- **Judge Agent**: Impartially evaluates the debate after 2 rounds, summarizing key arguments and declaring a logical winner.

## Project Structure

```
├── debate_app.py      # Main application and LangGraph workflow
├── requirements.txt   # Python dependencies
├── .env.example       # Example environment configuration
└── README.md          # Project documentation
```

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yashkirtisingh1789/Multi-Agent-Debate-System.git
   cd Multi-Agent-Debate-System
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   ```bash
   cp .env.example .env
   ```
   Add your OpenAI API key to `.env`:
   ```env
   OPENAI_API_KEY="sk-..."
   ```

## Running the Debate

Execute the debate script:
```bash
python debate_app.py
```
