#!/usr/bin/env python3
"""Create placeholder silent WAV files for testing"""

import os
import sys
from pathlib import Path

try:
    from pydub import AudioSegment
    from pydub.generators import Sine
except ImportError:
    print("Error: pydub not found. Install with: pip install pydub", file=sys.stderr)
    sys.exit(1)

# Track files needed
JUNGLE_TRACKS = [
    'jungle-ambient.wav',
    'jungle-birds.wav',
    'jungle-rain.wav',
    'jungle-insects.wav'
]

GROOVY_TRACKS = [
    'groovy-bass.wav',
    'groovy-rhythm.wav',
    'groovy-lead.wav'
]

def create_silent_wav(duration_seconds=60, sample_rate=44100, channels=2):
    """Create a silent WAV file"""
    # Create silent audio segment
    silence = AudioSegment.silent(duration=duration_seconds * 1000)  # pydub uses milliseconds
    return silence

def create_placeholder_track(output_path, duration=60):
    """Create a placeholder track (silent or very quiet tone)"""
    try:
        # Option 1: Completely silent
        audio = create_silent_wav(duration_seconds=duration)
        
        # Option 2: Very quiet tone (almost silent) - uncomment to use
        # tone = Sine(20).to_audio_segment(duration=duration * 1000)
        # tone = tone - 60  # Very quiet (-60dB)
        # audio = tone
        
        # Export as WAV (44.1kHz, 16-bit, stereo)
        audio.export(output_path, format="wav", parameters=["-ar", "44100", "-ac", "2"])
        return True
    except Exception as e:
        print(f"Error creating {output_path}: {e}", file=sys.stderr)
        return False

def main():
    """Create placeholder tracks"""
    # Get project directories
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    public_dir = project_root / 'public'
    public_dir.mkdir(exist_ok=True)
    
    print("Creating placeholder WAV files...")
    print("(These will be silent - no actual audio content)\n")
    
    all_tracks = JUNGLE_TRACKS + GROOVY_TRACKS
    created = 0
    skipped = 0
    
    for track_name in all_tracks:
        output_path = public_dir / track_name
        
        if output_path.exists():
            print(f"  SKIP: {track_name} (already exists)")
            skipped += 1
            continue
        
        if create_placeholder_track(output_path, duration=60):
            file_size = output_path.stat().st_size / (1024 * 1024)  # MB
            print(f"  OK:   {track_name} ({file_size:.2f} MB)")
            created += 1
        else:
            print(f"  FAIL: {track_name}")
    
    print(f"\nCreated {created} files, skipped {skipped} existing files")
    print(f"\nNote: These are silent placeholder files for testing.")
    print(f"Replace them with actual audio files when available.")

if __name__ == "__main__":
    main()
