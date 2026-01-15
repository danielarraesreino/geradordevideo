#!/usr/bin/env python3
"""
Teste de conexão ElevenLabs
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

def test_elevenlabs(api_key):
    """Testa conexão com ElevenLabs"""
    
    # Endpoint para user info (mais leve que listar todas as vozes)
    url = "https://api.elevenlabs.io/v1/user"
    
    headers = {
        "xi-api-key": api_key
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            subscription = data.get('subscription', {})
            
            print(f"✅ CONEXÃO BEM-SUCEDIDA!")
            print(f"👤 Usuário: {data.get('first_name', 'Unknown')}")
            print(f"💰 Tier: {subscription.get('tier', 'unknown')}")
            print(f"📊 Caracteres usados: {subscription.get('character_count', 0)}")
            print(f"🎯 Limite: {subscription.get('character_limit', 0)}")
            
            return True
        else:
            print(f"❌ Erro {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    print("\n🎙️  Testando ElevenLabs API...\n")
    
    api_key = load_api_key()
    
    if not api_key:
        print("❌ API key não encontrada no .env")
        sys.exit(1)
    
    print(f"🔑 API Key: {api_key[:20]}...")
    
    if test_elevenlabs(api_key):
        print(f"\n✅ ElevenLabs configurado com sucesso!")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
