#!/usr/bin/env python3
"""
Geração de Áudio Direta - ElevenLabs
Tenta gerar áudio mesmo se a verificação de usuário falhar
"""

import os
import sys
import requests
from pathlib import Path

def load_api_key():
    env_path = Path(__file__).parent.parent / '.env'
    with open(env_path, 'r') as f:
        for line in f:
            if line.startswith('ELEVENLABS_API_KEY='):
                return line.split('=', 1)[1].strip()
    return None

def generate_audio(api_key, text, output_path):
    """Gera áudio usando voice ID da Rachel"""
    
    voice_id = "21m00Tcm4TlvDq8ikWAM" # Rachel
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
    
    print(f"📡 Enviando requisição de áudio ({len(text)} chars)...")
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        return True
    else:
        print(f"❌ Erro {response.status_code}: {response.text}")
        return False

def main():
    print("\n🎙️  Gerando Áudio - História #002 (Maria)\n")
    
    # Carregar roteiro
    script_path = Path(__file__).parent.parent / 'output' / 'roteiro_002_exclusão_financeira.txt'
    if not script_path.exists():
        print("❌ Roteiro não encontrado")
        sys.exit(1)
        
    text = script_path.read_text(encoding='utf-8')
    
    # Carregar API key
    api_key = load_api_key()
    if not api_key:
        print("❌ API key não encontrada")
        sys.exit(1)
    
    # Output path
    output_dir = Path(__file__).parent.parent / 'output' / 'audio'
    output_dir.mkdir(exist_ok=True, parents=True)
    output_path = output_dir / 'audio_002.mp3'
    
    print(f"📝 Roteiro carregado: {script_path.name}")
    print(f"🔑 Usando API Key: {api_key[:15]}...")
    
    if generate_audio(api_key, text, output_path):
        print(f"\n✅ SUCESSO! Áudio gerado em: {output_path}")
        print(f"📂 Tamanho: {output_path.stat().st_size / 1024:.2f} KB")
        print("\n🎧 PRONTO PARA VÍDEO!")
    else:
        print("\n❌ Falha na geração. Verifique a chave ou quota.")
        sys.exit(1)

if __name__ == '__main__':
    main()
