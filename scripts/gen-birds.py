#!/usr/bin/env python3
"""Generate bird sounds as WAV file using audio synthesis"""

from pydub import AudioSegment
from pydub.generators import Sine, Square, Triangle
from pydub.effects import normalize
import os
import sys
import math
import random

# Bird sound parameters
SAMPLE_RATE = 44100
DURATION = 300  # 5 minutes of bird sounds
BIT_DEPTH = 16

def generate_chirp_freq(frequency, duration_ms, sample_rate=SAMPLE_RATE):
    """Generate a simple chirp using frequency modulation (no numpy)"""
    # Create base tone
    base_tone = Sine(frequency).to_audio_segment(duration=duration_ms)
    
    # Add slight variation with a modulated tone
    mod_freq = frequency * (1 + random.uniform(-0.15, 0.15))
    mod_tone = Sine(mod_freq).to_audio_segment(duration=duration_ms)
    
    # Mix tones for richness
    chirp = base_tone.overlay(mod_tone, gain_during_overlay=-6)  # Mix at -6dB
    
    # Apply amplitude envelope (fade in/out)
    fade_in = min(20, duration_ms // 10)  # 20ms or 10% fade in
    fade_out = min(50, duration_ms // 5)  # 50ms or 20% fade out
    chirp = chirp.fade_in(fade_in).fade_out(fade_out)
    
    return chirp

def generate_bird_call(frequency_range=(800, 4000), duration_ms_range=(50, 300)):
    """Generate a complete bird call (multiple chirps)"""
    num_chirps = random.randint(2, 6)  # 2-6 chirps per call
    call_chirps = []
    
    for i in range(num_chirps):
        # Frequency varies between chirps (melodic pattern)
        freq_factor = 1.0 + (i / num_chirps) * random.uniform(-0.3, 0.3)
        freq = random.uniform(*frequency_range) * freq_factor
        
        # Chirp duration
        chirp_duration = random.uniform(*duration_ms_range)
        
        # Generate chirp
        chirp = generate_chirp_freq(freq, int(chirp_duration))
        call_chirps.append(chirp)
        
        # Silence between chirps (except last one)
        if i < num_chirps - 1:
            silence_duration = random.uniform(30, 150)  # 30-150ms silence
            silence = AudioSegment.silent(duration=int(silence_duration))
            call_chirps.append(silence)
    
    # Concatenate all chirps
    call = sum(call_chirps)  # pydub's sum concatenates AudioSegments
    return call

def generate_descending_whistle(frequency_range=(1500, 3500), duration_ms=300):
    """Generate a descending whistle call"""
    start_freq = random.uniform(*frequency_range)
    end_freq = start_freq * random.uniform(0.5, 0.8)  # Descend 20-50%
    
    # Create multiple segments for smooth frequency transition
    segments = []
    num_segments = 10
    for i in range(num_segments):
        t = i / num_segments
        freq = start_freq + (end_freq - start_freq) * t
        segment_duration = duration_ms / num_segments
        segment = Sine(freq).to_audio_segment(duration=int(segment_duration))
        segments.append(segment)
    
    whistle = sum(segments)
    whistle = whistle.fade_in(20).fade_out(50)
    return whistle

def generate_warbling_trill(frequency_base=2000, duration_ms=400):
    """Generate a warbling trill (rapid frequency modulation)"""
    segments = []
    num_segments = 20  # Many small segments for warbling effect
    
    for i in range(num_segments):
        # Vary frequency around base
        variation = math.sin(i * 2 * math.pi / num_segments) * 0.2  # ±20% variation
        freq = frequency_base * (1 + variation)
        segment_duration = duration_ms / num_segments
        segment = Sine(freq).to_audio_segment(duration=int(segment_duration))
        segments.append(segment)
    
    trill = sum(segments)
    trill = trill.fade_in(10).fade_out(30)
    return trill

def generate_bird_sounds(duration_seconds=300, sample_rate=SAMPLE_RATE):
    """Generate continuous bird sounds for specified duration"""
    audio_segments = []
    current_duration_ms = 0
    target_duration_ms = duration_seconds * 1000
    
    # Different bird types (frequency ranges and call patterns)
    bird_patterns = [
        ('high_songbird', (1200, 3500), (50, 250)),
        ('medium_songbird', (800, 2500), (80, 400)),
        ('lower_songbird', (600, 1800), (100, 500)),
        ('whistle', (1500, 3500), (200, 400)),
        ('trill', (1800, 2800), (300, 600)),
    ]
    
    pattern_weights = [3, 3, 2, 2, 1]  # Weighted random selection
    
    while current_duration_ms < target_duration_ms:
        # Choose bird pattern (weighted random)
        pattern_idx = random.choices(range(len(bird_patterns)), weights=pattern_weights)[0]
        pattern_name, freq_range, duration_range = bird_patterns[pattern_idx]
        
        # Generate call based on pattern
        if pattern_name == 'whistle':
            call = generate_descending_whistle(freq_range, random.uniform(*duration_range))
        elif pattern_name == 'trill':
            call = generate_warbling_trill(random.uniform(*freq_range), random.uniform(*duration_range))
        else:
            call = generate_bird_call(freq_range, duration_range)
        
        audio_segments.append(call)
        current_duration_ms += len(call)
        
        # Variable silence between calls (natural timing)
        silence_duration = random.uniform(500, 3000)  # 0.5-3 seconds
        silence = AudioSegment.silent(duration=int(silence_duration))
        audio_segments.append(silence)
        current_duration_ms += silence_duration
        
        # Occasional longer pause (natural behavior)
        if random.random() < 0.1:  # 10% chance
            long_pause = random.uniform(2000, 5000)  # 2-5 seconds
            silence = AudioSegment.silent(duration=int(long_pause))
            audio_segments.append(silence)
            current_duration_ms += long_pause
    
    # Concatenate all segments
    print("Combining audio segments...")
    full_audio = sum(audio_segments)
    
    # Trim to exact duration
    target_samples = target_duration_ms
    if len(full_audio) > target_samples:
        full_audio = full_audio[:target_samples]
    
    # Normalize to prevent clipping (pydub's normalize)
    full_audio = normalize(full_audio, headroom=1.0)  # 1dB headroom
    
    return full_audio

def generate_bird_sounds_file(output_path=None, duration_seconds=300):
    """Generate bird sounds and save as WAV file"""
    try:
        print(f"Generating {duration_seconds} seconds of bird sounds...")
        print("This may take a moment...")
        
        # Generate audio
        audio_segment = generate_bird_sounds(duration_seconds, SAMPLE_RATE)
        
        # Determine output path
        if output_path is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(script_dir)
            public_dir = os.path.join(project_root, "public")
            output_path = os.path.join(public_dir, "jungle-birds.wav")
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Export as WAV (44.1kHz, 16-bit, mono)
        print("Saving to WAV file...")
        audio_segment.export(
            output_path,
            format="wav",
            parameters=["-ar", str(SAMPLE_RATE), "-ac", "1"]  # Mono
        )
        
        print(f"Bird sounds saved to {output_path}")
        
        # Get file info
        file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
        duration_actual = len(audio_segment) / 1000.0
        print(f"File size: {file_size_mb:.2f} MB")
        print(f"Duration: {duration_actual:.1f} seconds")
        print(f"Sample rate: {SAMPLE_RATE} Hz, {BIT_DEPTH}-bit, mono")
        
        return output_path
    
    except Exception as e:
        print(f"Error generating bird sounds: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate bird sounds as WAV file')
    parser.add_argument('--output', '-o', type=str, default=None,
                       help='Output WAV file path (default: public/jungle-birds.wav)')
    parser.add_argument('--duration', '-d', type=int, default=300,
                       help='Duration in seconds (default: 300 = 5 minutes)')
    args = parser.parse_args()
    
    generate_bird_sounds_file(args.output, args.duration)
