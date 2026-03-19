# history_manager.py

import json
import os
from datetime import datetime


HISTORY_FOLDER = "chat_histories"


def ensure_folder():
    if not os.path.exists(HISTORY_FOLDER):
        os.makedirs(HISTORY_FOLDER)


def save_chat(messages: list, filename: str = None) -> str:
    ensure_folder()
    if not filename:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"chat_{timestamp}.json"
    filepath = os.path.join(HISTORY_FOLDER, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)
    return filename


def load_chat(filename: str) -> list:
    filepath = os.path.join(HISTORY_FOLDER, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def list_chats() -> list:
    ensure_folder()
    files = [f for f in os.listdir(HISTORY_FOLDER) if f.endswith(".json")]
    files.sort(reverse=True)
    return files


def delete_chat(filename: str):
    filepath = os.path.join(HISTORY_FOLDER, filename)
    if os.path.exists(filepath):
        os.remove(filepath)