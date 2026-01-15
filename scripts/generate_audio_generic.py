#!/usr/bin/env python3
"""
Geração de Áudio Direta - ElevenLabs (Genérico)
"""

import os
import sys
import argparse
import requests
from pathlib import Path

def load_api_key():
    env_path = Path(__file__).parent.parent / '.env'
    with open(env_path, 'r') as f:
        for line in f:
            if line.startswith('ELEVENLABS_API_KEY='):
                return line.split('=', 1)[1].strip()
    return None

def generate_audio(api_key, text, output_path, voice="adam"):
    """Gera áudio usando voice ID"""
    
    voices = {
        "rachel": "21m00Tcm4TlvDq8ikWAM",
        "adam": "pNInz6obpgDQGcFmaJgB" # Voz masculina profunda
    }
    
    voice_id = voices.get(voice, voices["rachel"])
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    print(f"📡 Gerando voz '{voice}' ({len(text)} chars)...")
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        return True
    else:
        print(f"❌ Erro {response.status_code}: {response.text}")
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("script_path", help="Caminho do roteiro")
    parser.add_argument("story_id", help="ID da história")
    parser.add_argument("--voice", default="adam", help="Voz (rachel/adam)")
    args = parser.parse_args()
    
    # Carregar roteiro
    script = Path(args.script_path).read_text(encoding='utf-8')
    
    api_key = load_api_key()
    if not api_key:
        print("❌ API key não encontrada")
        sys.exit(1)
    
    output_dir = Path(__file__).parent.parent / 'output' / 'audio'
    output_dir.mkdir(exist_ok=True, parents=True)
    output_path = output_dir / f'audio_{args.story_id}.mp3'
    
    if generate_audio(api_key, script, output_path, args.voice):
        print(f"✅ Áudio salvo: {output_path}")

if __name__ == '__main__':
    main()
