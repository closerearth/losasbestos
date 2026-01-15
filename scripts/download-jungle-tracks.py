#!/usr/bin/env python3
"""Download rainforest sound tracks from earth.fm and convert to WAV format"""

import os
import sys
import subprocess
from pathlib import Path

# Track mapping: target filename -> description/search terms
JUNGLE_TRACKS = {
    'jungle-ambient.wav': 'ambient rainforest',
    'jungle-birds.wav': 'rainforest birds',
    'jungle-rain.wav': 'rainforest rain',
    'jungle-insects.wav': 'rainforest insects'
}

GROOVY_TRACKS = {
    'groovy-bass.wav': 'bass',
    'groovy-rhythm.wav': 'rhythm',
    'groovy-lead.wav': 'lead'
}

def check_ytdlp():
    """Check if yt-dlp is installed"""
    try:
        result = subprocess.run(['yt-dlp', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return 'yt-dlp'
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    try:
        result = subprocess.run(['youtube-dl', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return 'youtube-dl'
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    return None

def download_from_url(url, output_path, tool='yt-dlp'):
    """Download audio from URL and convert to WAV"""
    try:
        print(f"Downloading from {url}...")
        
        # Use yt-dlp/youtube-dl to extract and download
        # Extract best audio quality and convert to WAV
        cmd = [
            tool,
            url,
            '--extract-audio',
            '--audio-format', 'wav',
            '--audio-quality', '0',  # Best quality
            '--output', str(output_path),
            '--no-playlist',  # Single file only
            '--quiet',  # Less verbose output
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            # yt-dlp may add extension, check if file exists
            if output_path.exists():
                return True
            
            # Try with .wav extension added by yt-dlp
            wav_path = output_path.parent / f"{output_path.stem}.wav"
            if wav_path.exists():
                wav_path.rename(output_path)
                return True
        else:
            print(f"Error: {result.stderr}", file=sys.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"Timeout downloading {url}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error downloading {url}: {e}", file=sys.stderr)
        return False

def main():
    """Main function to download tracks"""
    # Get project directories
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    public_dir = project_root / 'public'
    public_dir.mkdir(exist_ok=True)
    
    # Check for yt-dlp or youtube-dl
    tool = check_ytdlp()
    if not tool:
        print("Error: yt-dlp or youtube-dl not found!", file=sys.stderr)
        print("\nInstall with:")
        print("  macOS: brew install yt-dlp")
        print("  Linux: sudo apt-get install yt-dlp")
        print("  Python: pip install yt-dlp")
        sys.exit(1)
    
    print(f"Using {tool} to download tracks...")
    
    # Earth.fm playlist URL
    playlist_url = "https://earth.fm/playlists/rainforest-sounds/"
    
    print(f"\nNote: earth.fm doesn't provide direct downloads.")
    print(f"This script will attempt to extract audio from the playlist page.")
    print(f"If that fails, you may need to:")
    print(f"  1. Use the earth.fm mobile app for offline listening")
    print(f"  2. Find alternative free sources for rainforest audio")
    print(f"  3. Use freesound.org or similar free audio libraries\n")
    
    # For now, provide instructions
    print("=" * 60)
    print("DOWNLOAD INSTRUCTIONS:")
    print("=" * 60)
    print("\nEarth.fm doesn't allow direct downloads from their website.")
    print("Here are alternative options:\n")
    print("Option 1: Use FreeSound.org (CC0/CC-BY licensed)")
    print("  - Visit https://freesound.org/")
    print("  - Search for: 'rainforest', 'jungle birds', 'rain sounds', 'insects'")
    print("  - Filter by: CC0 License (public domain)")
    print("  - Download and save to public/ with these names:")
    for filename in JUNGLE_TRACKS.keys():
        print(f"    - {filename}")
    print("\nOption 2: Create placeholder silent files (for testing)")
    print("  Run: python scripts/create-placeholder-tracks.py")
    print("\nOption 3: Use earth.fm mobile app")
    print("  - Download the iOS app")
    print("  - Enable offline mode")
    print("  - Extract audio from app (advanced)\n")
    
    # Ask user if they want to try yt-dlp anyway
    response = input("Try downloading with yt-dlp anyway? (y/n): ").strip().lower()
    if response == 'y':
        output_file = public_dir / 'jungle-test.wav'
        if download_from_url(playlist_url, output_file, tool):
            print(f"Successfully downloaded to {output_file}")
        else:
            print("Download failed. Please use one of the alternative options above.")
    else:
        print("Skipping download. Please use one of the alternative options above.")

if __name__ == "__main__":
    main()
