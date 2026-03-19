import sys
import shutil


def test_ffmpeg():
    """Test if FFmpeg is accessible."""
    print("🔍 Testing FFmpeg...")
    ffmpeg = shutil.which("ffmpeg")

    if ffmpeg:
        print(f"  ✓ FFmpeg found at: {ffmpeg}")
        return True
    else:
        print(f"  ✗ FFmpeg NOT found in PATH")
        print(f"\n  💡 Quick fix:")
        print(f"     pip install ffmpeg-python pydub")
        print(f"\n  Or try restarting your terminal first!")
        return False


def test_whisper():
    """Test if Whisper model loads."""
    print("\n🎙️ Testing Whisper model...")
    try:
        import whisper
        print(f"  ✓ Whisper imported successfully")

        print(f"  ⏳ Loading 'small' model (this may take a moment)...")
        model = whisper.load_model("small")
        print(f"  ✓ Whisper model loaded successfully!")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_dependencies():
    """Test all required packages."""
    print("\n📦 Testing dependencies...")
    packages = [
        ("streamlit", "streamlit"),
        ("whisper", "openai-whisper"),
        ("streamlit_mic_recorder", "streamlit-mic-recorder"),
        ("pydub", "pydub"),
        ("pypdf", "pypdf"),
        ("openai", "openai"),
    ]

    all_ok = True
    for module_name, pip_name in packages:
        try:
            __import__(module_name)
            print(f"  ✓ {module_name}")
        except ImportError:
            print(f"  ✗ {module_name} - run: pip install {pip_name}")
            all_ok = False

    return all_ok


def main():
    print("=" * 60)
    print("🤖 Local AI Chatbot - Setup Verification")
    print("=" * 60)

    deps_ok = test_dependencies()
    ffmpeg_ok = test_ffmpeg()
    whisper_ok = test_whisper()

    print("\n" + "=" * 60)

    if deps_ok and ffmpeg_ok and whisper_ok:
        print("✅ Everything looks good!")
        print("\n🚀 Run your app with:")
        print("   streamlit run app.py")
        return 0
    else:
        print("❌ Some issues detected. Check above for fixes.")
        print("\n⚡ Most common issue:")
        print("   FFmpeg not in PATH - restart your terminal/IDE!")
        return 1


if __name__ == "__main__":
    sys.exit(main())