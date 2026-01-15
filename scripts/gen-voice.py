#!/usr/bin/env python3
"""Generate Fire Horse speech as WAV file using Google TTS"""

from gtts import gTTS
from pydub import AudioSegment
import io
import os
import sys
try:
    import sounddevice as sd
    SOUNDDEVICE_AVAILABLE = True
except ImportError:
    SOUNDDEVICE_AVAILABLE = False

# The Fire Horse script with micro-jokes
script = """Friends, fellow travelers, and anyone who accidentally clicked this link.

Tonight we call in the Fire Horse. Not as some dusty myth, but as a force of becoming. Also, arguably, the best excuse for a party in sixty years.

The Fire Horse is movement and ignition. It's that moment when Netflix asks if you're still watching and you say no, actually, I'm going outside. It is courage without permission. Life refusing to shrink. Spreadsheets refusing to define us.

In every culture, the horse has been a bridge: between human and wild, between earth and horizon, between instinct and that thing your therapist keeps asking about.

And fire? Fire is transformation. It clears what is stagnant. It tempers what is raw. It also makes excellent s'mores, but that's beside the point.

Together, Fire and Horse are not chaos. They are momentum with purpose. Think less "everything is on fire" and more "controlled burn with good vibes."

We stand at the edge of an era that has exhausted itself. An era of separation: humans from nature, economies from ecology, work emails from any sense of meaning whatsoever.

The Fire Horse does not ask politely for change. It arrives when systems can no longer pretend they are alive. When algorithms recommend you videos of algorithms. When your smart fridge judges your midnight cheese habits.

This is not an ending. This is a reboot. The good kind, not the Hollywood kind.

A remembering.

The Fire Horse teaches us that humanity was never meant to dominate nature, nor disappear into it, but to dance with it. Awkwardly at first, sure. Everyone's awkward at first.

To become keystone species again. Caretakers with creativity. Engineers with reverence. People who compost and won't shut up about it, but in a charming way.

Playfulness returns here. Because regeneration is not grim labor. It is joyful participation in life's intelligence. If you're not occasionally laughing, you might be doing it wrong.

Soil rebuilding itself. Water finding new paths. Communities re-learning how to trust, or at least how to share tools without being weird about it.

Laughter is not a distraction from the work. It is proof the work is aligned. The mycelium network definitely has inside jokes. We just can't hear them yet.

And yes, we carry tools now our ancestors could not imagine. They also couldn't imagine TikTok, so let's use discernment.

Technology is not the enemy of nature. Extraction is. When technology serves life, it becomes a liberation tool. When it serves engagement metrics, it becomes a problem.

Sensors that listen to forests. Networks that coordinate stewardship. Systems that reward regeneration instead of quarterly growth. Revolutionary stuff. Also: common sense, if you think about it.

The Fire Horse does not reject technology. It tames it, rides it, occasionally checks its screen time and sighs deeply.

This is a call to boldness. Not recklessness. Boldness. There's a difference. Look it up. Actually, you probably shouldn't look it up right now. Stay present.

To live faster where life needs speed, and slower where wisdom grows. To know the difference. To stop doom-scrolling. Seriously. This is your sign.

To choose courage over comfort. Regeneration over convenience. Actual community over followers.

The Fire Horse runs with those who refuse to be small. Who dare to imagine civilizations that last seven generations, not seven news cycles.

So let us run. Not from anything. Toward something.

With the land beneath us. With the fire within us. With technology in service, not command. With snacks, probably. Revolutions need snacks.

May we merge back into the living world. Not by losing ourselves, but by finally becoming fully human. Which, for the record, includes rest. And joy. And the occasional terrible pun.

Welcome, Fire Horse. Run through us. Try not to knock over the furniture."""

def list_microphones():
    """Detect and list all available microphone devices.
    
    Returns:
        List of dictionaries with microphone device information
    """
    if not SOUNDDEVICE_AVAILABLE:
        print("sounddevice not available. Install with: pip install sounddevice", file=sys.stderr)
        return []
    
    try:
        devices = sd.query_devices()
        microphones = []
        
        for i, device in enumerate(devices):
            if device['max_input_channels'] > 0:
                mic_info = {
                    'index': i,
                    'name': device['name'],
                    'channels': device['max_input_channels'],
                    'sample_rate': device['default_samplerate'],
                    'hostapi': sd.query_hostapis(device['hostapi'])['name'],
                    'is_default': (i == sd.default.device[0])
                }
                microphones.append(mic_info)
        
        return microphones
    except Exception as e:
        print(f"Error detecting microphones: {e}", file=sys.stderr)
        return []

def display_microphones():
    """Display all available microphones with their information."""
    microphones = list_microphones()
    
    if not microphones:
        print("No microphones detected.")
        return
    
    print(f"\n{'='*70}")
    print(f"Detected {len(microphones)} microphone device(s):")
    print(f"{'='*70}\n")
    
    for mic in microphones:
        default_marker = " [DEFAULT]" if mic['is_default'] else ""
        print(f"Device {mic['index']}: {mic['name']}{default_marker}")
        print(f"  Channels: {mic['channels']}")
        print(f"  Sample Rate: {mic['sample_rate']:.0f} Hz")
        print(f"  Host API: {mic['hostapi']}")
        print()
    
    return microphones

def get_microphone_control(mic_index=None):
    """Get microphone device control information.
    
    Args:
        mic_index: Index of microphone device. If None, returns default.
    
    Returns:
        Dictionary with microphone control settings
    """
    if not SOUNDDEVICE_AVAILABLE:
        return None
    
    if mic_index is None:
        mic_index = sd.default.device[0] if sd.default.device[0] is not None else 0
    
    try:
        device = sd.query_devices(mic_index)
        if device['max_input_channels'] == 0:
            print(f"Device {mic_index} is not an input device.", file=sys.stderr)
            return None
        
        return {
            'index': mic_index,
            'name': device['name'],
            'channels': device['max_input_channels'],
            'sample_rate': device['default_samplerate'],
            'device_info': device
        }
    except Exception as e:
        print(f"Error getting microphone control: {e}", file=sys.stderr)
        return None

def generate_speech(output_path=None):
    """Generate speech from script and save as WAV file.
    
    Args:
        output_path: Path to output WAV file. If None, saves to public directory.
    
    Returns:
        Path to generated WAV file
    """
    try:
        print("Generating speech with Google TTS...")
        
        # Use UK English for a warmer tone
        tts = gTTS(text=script, lang='en', tld='co.uk', slow=False)
        
        # Save to MP3 first (gTTS outputs MP3)
        mp3_buffer = io.BytesIO()
        tts.write_to_fp(mp3_buffer)
        mp3_buffer.seek(0)
        
        print("Converting to WAV...")
        
        # Convert MP3 to WAV using pydub
        audio = AudioSegment.from_mp3(mp3_buffer)
        
        # Determine output path
        if output_path is None:
            # Save to public directory
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(script_dir)  # Go up from scripts/ to project root
            public_dir = os.path.join(project_root, "public")
            wav_path = os.path.join(public_dir, "fire-horse-speech.wav")
        else:
            wav_path = output_path
        
        # Export as WAV (44.1kHz, 16-bit)
        audio.export(wav_path, format="wav")
        
        print(f"Speech saved to {wav_path}")
        
        # Get duration
        duration = len(audio) / 1000.0
        print(f"Duration: {duration:.1f} seconds")
        
        return wav_path
    
    except Exception as e:
        print(f"Error generating speech: {e}", file=sys.stderr)
        print("\nNote: pydub requires ffmpeg to convert MP3 to WAV.")
        print("Install ffmpeg with:")
        print("  macOS: brew install ffmpeg")
        print("  Linux: sudo apt-get install ffmpeg")
        print("  Windows: Download from https://ffmpeg.org/download.html")
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate Fire Horse speech as WAV file')
    parser.add_argument('--list-mics', action='store_true', 
                       help='List all available microphone devices')
    parser.add_argument('--output', '-o', type=str, default=None,
                       help='Output WAV file path (default: public/fire-horse-speech.wav)')
    args = parser.parse_args()
    
    if args.list_mics:
        display_microphones()
    else:
        # Display microphones for reference
        mics = display_microphones()
        if mics:
            print("Generating speech...")
        print()
        generate_speech(output_path=args.output)