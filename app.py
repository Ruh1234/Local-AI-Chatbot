# app.py

import streamlit as st
from chatbot import chat, get_initial_history
from history_manager import save_chat, load_chat, list_chats, delete_chat
from streamlit_mic_recorder import mic_recorder
from voice_input import transcribe_audio

st.set_page_config(page_title="Local AI Chatbot", page_icon="🤖", layout="wide")

if "history" not in st.session_state:
    st.session_state.history = get_initial_history()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_chat_name" not in st.session_state:
    st.session_state.current_chat_name = None

if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🤖 My Chats")

    if st.button("➕ New conversation", use_container_width=True):
        if st.session_state.messages:
            save_chat(st.session_state.messages, st.session_state.current_chat_name)
        st.session_state.history = get_initial_history()
        st.session_state.messages = []
        st.session_state.current_chat_name = None
        st.rerun()

    st.divider()

    saved_chats = list_chats()

    if saved_chats:
        for chat_file in saved_chats:
            display_name = chat_file.replace(".json", "").replace("_", " ")
            col1, col2 = st.columns([5, 1])

            with col1:
                is_active = st.session_state.current_chat_name == chat_file
                label = f"**{display_name}**" if is_active else display_name
                if st.button(label, key=f"load_{chat_file}", use_container_width=True):
                    loaded = load_chat(chat_file)
                    st.session_state.messages = loaded
                    st.session_state.current_chat_name = chat_file
                    st.session_state.history = get_initial_history()
                    for msg in loaded:
                        st.session_state.history.append({
                            "role": msg["role"],
                            "content": msg["content"]
                        })
                    st.rerun()

            with col2:
                if st.button("🗑️", key=f"del_{chat_file}"):
                    delete_chat(chat_file)
                    if st.session_state.current_chat_name == chat_file:
                        st.session_state.messages = []
                        st.session_state.history = get_initial_history()
                        st.session_state.current_chat_name = None
                    st.rerun()
    else:
        st.caption("No saved chats yet. Start chatting!")

    st.divider()

    st.markdown("**💾 Save as**")
    custom_name = st.text_input("", placeholder="e.g. work_notes", label_visibility="collapsed")
    if st.button("Save", use_container_width=True):
        if st.session_state.messages:
            filename = f"{custom_name}.json" if custom_name else None
            saved_as = save_chat(st.session_state.messages, filename)
            st.session_state.current_chat_name = saved_as
            st.success("Saved!")
            st.rerun()
        else:
            st.warning("Nothing to save yet!")

    st.divider()
    st.markdown("**Model:** `llama-3.3-70b`")
    st.markdown("🔒 Runs locally")

# ── Main chat area ────────────────────────────────────────────
st.title("🤖 Local AI Chatbot")
st.caption("Powered by NVIDIA + Ollama — simple and clean")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── File uploader ─────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Attach a file (optional)",
    type=["txt", "pdf", "py", "csv", "md"],
    label_visibility="collapsed"
)

file_content = ""
file_name = ""
if uploaded_file is not None:
    file_name = uploaded_file.name
    try:
        if uploaded_file.name.endswith(".pdf"):
            import pypdf, io
            reader = pypdf.PdfReader(io.BytesIO(uploaded_file.read()))
            file_content = "\n".join(
                page.extract_text() for page in reader.pages
                if page.extract_text()
            )
        else:
            file_content = uploaded_file.read().decode("utf-8")

        if file_content:
            st.success(f"✅ File ready: {file_name} ({len(file_content)} characters extracted)")
        else:
            st.warning("No text could be extracted from this file.")

    except Exception as e:
        st.warning(f"Could not read file: {e}")
        file_content = ""

# ── Voice input ───────────────────────────────────────────────
# NEW - replace with this
st.markdown("🎙️ **Or speak your message:**")
audio = mic_recorder(
    start_prompt="Click to record",
    stop_prompt="Recording... click to stop",
    key="recorder"
)

if audio and audio["bytes"]:
    with st.spinner("Transcribing your voice..."):
        transcribed = transcribe_audio(audio["bytes"])
        if transcribed:
            st.session_state.voice_text = transcribed
            st.info(f'Heard: "{transcribed}"')

# ── Chat input ────────────────────────────────────────────────
user_input = st.chat_input("Ask me anything...")

# Use voice text if no typed input
final_input = user_input or (st.session_state.voice_text if st.session_state.voice_text else None)

if final_input:
    st.session_state.voice_text = ""

    with st.chat_message("user"):
        st.markdown(final_input)
        if file_content:
            st.caption(f"📎 {file_name}")
    st.session_state.messages.append({"role": "user", "content": final_input})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply, st.session_state.history = chat(
                user_message=final_input,
                history=st.session_state.history,
                file_content=file_content,
                file_name=file_name
            )
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})

    if st.session_state.current_chat_name:
        save_chat(st.session_state.messages, st.session_state.current_chat_name)

