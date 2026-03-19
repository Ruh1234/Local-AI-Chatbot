#!/usr/bin/env python3
"""
Simple FFmpeg setup and verification
Run this to fix the FFmpeg warning
"""

import os
import sys
import shutil
import subprocess
import platform


def find_ffmpeg():
    """Find FFmpeg in system."""
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        print(f"✓ FFmpeg found at: {ffmpeg}")
        return ffmpeg
    else:
        print("✗ FFmpeg not found in PATH")
        return None


def test_ffmpeg(ffmpeg_path):
    """Test if FFmpeg works."""
    try:
        result = subprocess.run(
            [ffmpeg_path, "-version"],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            print("✓ FFmpeg is working")
            return True
    except:
        pass
    print("✗ FFmpeg not working")
    return False


def main():
    print("=" * 50)
    print("🎬 FFmpeg Check")
    print("=" * 50)

    ffmpeg = find_ffmpeg()

    if not ffmpeg:
        print("\n❌ FFmpeg NOT found!\n")
        print("FIX OPTIONS:")
        print("-" * 50)

        if platform.system() == "Windows":
            print("\n1. Using Chocolatey (Easiest):")
            print("   choco install ffmpeg")

            print("\n2. Manual Download:")
            print("   • Go to: https://www.gyan.dev/ffmpeg/builds/")
            print("   • Download 'Full' build")
            print("   • Extract to: C:\\ffmpeg")
            print("   • Add C:\\ffmpeg\\bin to Windows PATH")
            print("   • Restart terminal/IDE")

            print("\n3. Python Package:")
            print("   pip install ffmpeg-python")

        print("\nAfter fixing, restart terminal and run this again:")
        print("   python fix_ffmpeg.py")
        return 1

    # Test it
    if not test_ffmpeg(ffmpeg):
        print("\nFFmpeg found but not working properly")
        return 1

    print("\n✅ FFmpeg is ready to use!")
    print("\nYou can now run:")
    print("   streamlit run app.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())