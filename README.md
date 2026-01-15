# Hinoeuma: Generative Dark Techno DJ Toolbox

A rare combination — once every 60 years.

## Development

### Generate Audio Files

First, set up a Python virtual environment (recommended):

```bash
# Create virtual environment (one-time setup)
python3 -m venv venv

# Activate virtual environment (do this each time you work on the project)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Generate Fire Horse speech:**
```bash
source venv/bin/activate  # If not already activated
python scripts/gen-voice.py
```
This will generate `public/fire-horse-speech.wav` using Google Text-to-Speech.

**Generate bird sounds:**
```bash
source venv/bin/activate  # If not already activated
python scripts/gen-birds.py
```
This will generate `public/jungle-birds.wav` using audio synthesis. You can specify duration:
```bash
python scripts/gen-birds.py --duration 300  # 5 minutes (default)
python scripts/gen-birds.py --duration 60   # 1 minute
```

**Note:** Requires `ffmpeg` for audio conversion:
- macOS: `brew install ffmpeg`
- Linux: `sudo apt-get install ffmpeg`
- Windows: Download from https://ffmpeg.org/download.html

### Local Development

Serve the static files locally:

```bash
cd public
python3 -m http.server 8000
```

Then open http://localhost:8000 in your browser.

## Deployment

This project is configured for Vercel deployment.

### Deploy to Vercel

1. Install Vercel CLI (if not already installed):
   ```bash
   npm i -g vercel
   ```

2. Deploy:
   ```bash
   vercel
   ```

3. For production:
   ```bash
   vercel --prod
   ```

The `public/` directory will be served as the root directory.

### Project Structure

```
/
├── public/          # Static files (served as root)
│   ├── index.html   # Main application
│   ├── fire-horse-speech.wav
│   ├── robots.txt
│   └── sitemap.xml
├── scripts/         # Development scripts
│   └── gen-voice.py # Voice generation script
├── vercel.json      # Vercel configuration
└── requirements.txt # Python dependencies (dev only)
```

## Features

- **320kHz Lossless Audio** - Professional quality audio processing
- **Voice Narration** - Fire Horse speech with effects
- **Generative Techno** - Dark, industrial synthesizer
- **Jungle Ambience** - Environmental audio layers
- **Professional DJ Effects** - EQ, filters, reverb, distortion
