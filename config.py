# config.py

import os
from dotenv import load_dotenv

# Force load the .env file
load_dotenv(override=True)

# NVIDIA API settings
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

if not NVIDIA_API_KEY:
    raise ValueError("NVIDIA_API_KEY not found! Check your .env file.")

NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
MODEL_NAME = "meta/llama-3.3-70b-instruct"

TEMPERATURE = 0.7
SYSTEM_PROMPT = """You are a helpful, friendly general assistant.
You can read and analyze files that the user attaches.
When a file is provided, use its contents to answer the user's question.
Answer clearly and concisely."""
