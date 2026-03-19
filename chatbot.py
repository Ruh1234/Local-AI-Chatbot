# chatbot.py

from openai import OpenAI
from config import MODEL_NAME, TEMPERATURE, SYSTEM_PROMPT, NVIDIA_API_KEY, NVIDIA_BASE_URL


# Initialize the NVIDIA client
client = OpenAI(
    base_url=NVIDIA_BASE_URL,
    api_key=NVIDIA_API_KEY
)


def get_initial_history():
    """Returns a fresh conversation with the system prompt."""
    return [{"role": "system", "content": SYSTEM_PROMPT}]


def chat(user_message: str, history: list, file_content: str = "", file_name: str = "") -> tuple:
    """
    Send a message and get a reply from NVIDIA's API.

    Args:
        user_message: The user's input text.
        history: The full conversation history so far.
        file_content: Optional extracted text from an attached file.
        file_name: Optional name of the attached file.

    Returns:
        A tuple of (assistant_reply, updated_history)
    """
    # Build the full message including file content if provided
    if file_content:
        full_message = f"""I have attached a file called '{file_name}'. Here is the complete text content from it:

=== START OF FILE CONTENT ===
{file_content}
=== END OF FILE CONTENT ===

Based on the file content above, please answer this:
{user_message}"""
    else:
        full_message = user_message

    history.append({"role": "user", "content": full_message})

    # Call NVIDIA API
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=history,
        temperature=TEMPERATURE,
        max_tokens=1024
    )

    assistant_reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": assistant_reply})

    return assistant_reply, history



