#!/usr/bin/env python3
"""Generate music using AudioCraft's MusicGen model"""

import os
import sys
import argparse
from pathlib import Path

try:
    from audiocraft.models import MusicGen
    import torch
except ImportError as e:
    print(f"Error: Missing required dependency. Please install audiocraft:")
    print(f"  pip install audiocraft")
    sys.exit(1)

def generate_music(prompt, output_path, duration=30, model_size='facebook/musicgen-medium'):
    """Generate music using MusicGen model and save as WAV file
    
    Args:
        prompt: Text description of the music to generate
        output_path: Path to save the output WAV file
        duration: Duration of the generated music in seconds (default: 30)
        model_size: Model to use (default: 'facebook/musicgen-medium')
    """
    print(f"Loading MusicGen model: {model_size}")
    try:
        model = MusicGen.get_pretrained(model_size)
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Make sure you have internet connection for first-time model download")
        sys.exit(1)
    
    print(f"Setting generation parameters: duration={duration}s")
    model.set_generation_params(duration=duration)
    
    print(f"Generating music with prompt: '{prompt}'")
    try:
        wav = model.generate([prompt])
    except Exception as e:
        print(f"Error generating music: {e}")
        sys.exit(1)
    
    # Convert tensor to numpy array and save
    audio_array = wav[0].cpu().numpy()
    sample_rate = model.sample_rate
    
    # Save as WAV file using scipy or soundfile
    try:
        import scipy.io.wavfile as wavfile
        # Convert from float32 [-1, 1] to int16 [-32768, 32767]
        audio_int16 = (audio_array * 32767).astype('int16')
        wavfile.write(output_path, sample_rate, audio_int16)
        print(f"Successfully saved music to: {output_path}")
        print(f"  Duration: {duration}s")
        print(f"  Sample rate: {sample_rate}Hz")
    except ImportError:
        try:
            import soundfile as sf
            sf.write(output_path, audio_array, sample_rate)
            print(f"Successfully saved music to: {output_path}")
            print(f"  Duration: {duration}s")
            print(f"  Sample rate: {sample_rate}Hz")
        except ImportError:
            print("Error: Need either scipy or soundfile to save WAV file")
            print("  pip install scipy")
            print("  or")
            print("  pip install soundfile")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Generate music using AudioCraft MusicGen')
    parser.add_argument(
        '--prompt',
        type=str,
        default='dark minimal techno, 130bpm, rolling bassline',
        help='Text description of the music to generate (default: "dark minimal techno, 130bpm, rolling bassline")'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='public/generated-music.wav',
        help='Output WAV file path (default: public/generated-music.wav)'
    )
    parser.add_argument(
        '--duration',
        type=int,
        default=30,
        help='Duration in seconds (default: 30)'
    )
    parser.add_argument(
        '--model',
        type=str,
        default='facebook/musicgen-medium',
        choices=['facebook/musicgen-small', 'facebook/musicgen-medium', 'facebook/musicgen-large', 'facebook/musicgen-melody'],
        help='Model size to use (default: facebook/musicgen-medium)'
    )
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    generate_music(
        prompt=args.prompt,
        output_path=str(output_path),
        duration=args.duration,
        model_size=args.model
    )

if __name__ == '__main__':
    main()
