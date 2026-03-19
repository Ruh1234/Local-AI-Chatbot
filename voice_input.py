import whisper
import tempfile
import os
import shutil
from pathlib import Path

# Load the Whisper model once (cached)
try:
    model = whisper.load_model("small")
except Exception as e:
    print(f"Error loading Whisper model: {e}")
    model = None


def check_ffmpeg_installed() -> bool:
    """
    Check if FFmpeg is installed and in PATH.
    Returns True if found, False otherwise.
    """
    ffmpeg_path = shutil.which("ffmpeg")

    if ffmpeg_path:
        print(f"✓ FFmpeg found at: {ffmpeg_path}")
        return True
    else:
        print("❌ FFmpeg not installed or not in PATH!")
        print("\nQuick fix:")
        print("  1. Download from: https://ffmpeg.org/download.html")
        print("  2. Add to Windows PATH: C:\\ffmpeg\\bin")
        print("  3. Restart your IDE/terminal")
        print("\nOr run: pip install ffmpeg-python pydub")
        return False


def transcribe_audio(audio_bytes: bytes) -> str:
    """
    Convert recorded audio bytes to text using Whisper.

    Args:
        audio_bytes: Raw audio bytes from streamlit-mic-recorder

    Returns:
        Transcribed text as a string
    """
    try:
        # Check if model loaded
        if model is None:
            return "Error: Whisper model failed to load"

        # Check if FFmpeg is available (critical for Whisper)
        if not check_ffmpeg_installed():
            return "Error: FFmpeg is required but not installed. See instructions above."

        # Save audio bytes to a temporary .wav file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        try:
            print(f"📝 Transcribing audio from: {tmp_path}")

            # Transcribe using Whisper
            result = model.transcribe(
                tmp_path,
                language="en",  # Optional: specify language for faster processing
                verbose=False
            )

            transcribed_text = result.get("text", "").strip()

            if transcribed_text:
                print(f"✓ Transcription successful: {transcribed_text}")
                return transcribed_text
            else:
                print("⚠ No speech detected in audio")
                return "No speech detected. Please try again."

        finally:
            # Always clean up temp file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
                print(f"🗑️ Cleaned up temp file")

    except FileNotFoundError as e:
        print(f"❌ FileNotFoundError: {e}")
        if "ffmpeg" in str(e).lower():
            return "Error: FFmpeg not found. Please install it first."
        return f"Error: File not found: {e}"

    except Exception as e:
        error_type = type(e).__name__
        print(f"❌ {error_type}: {e}")
        return f"Could not transcribe audio: {error_type}: {e}"