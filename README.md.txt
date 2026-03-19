# 🤖 Local AI Chatbot

A conversational AI chatbot built with Python and Streamlit, powered by NVIDIA's Llama 3.3 70B model.

## Features
- 💬 Chat with a powerful AI (Llama 3.3 70B via NVIDIA API)
- 📎 Upload and analyze PDF, TXT, CSV, PY, MD files
- 🎙️ Voice input via browser microphone (no extra setup needed)
- 💾 Save and load chat history
- 🔒 Your data stays private

## Tech Stack
- Python
- Streamlit
- NVIDIA API (Llama 3.3 70B)
- pypdf (PDF extraction)

## How to Run
1. Clone the repo
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Add your NVIDIA API key to a `.env` file:
```
NVIDIA_API_KEY=your_key_here
```
4. Run the app:
```
streamlit run app.py
```

## Project Structure
- `app.py` — Streamlit web UI
- `chatbot.py` — Chat logic and NVIDIA API integration
- `config.py` — Settings and configuration
- `history_manager.py` — Save and load chat history

## License
MIT License