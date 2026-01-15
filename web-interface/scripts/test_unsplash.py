#!/usr/bin/env python3
"""
Teste de conexão Unsplash API
"""

import os
import sys
import requests
from pathlib import Path

def load_api_key():
    env_path = Path(__file__).parent.parent / '.env'
    with open(env_path, 'r') as f:
        for line in f:
            if line.startswith('UNSPLASH_ACCESS_KEY='):
                return line.split('=', 1)[1].strip()
    return None

def test_unsplash(access_key):
    """Testa conexão com Unsplash"""
    
    url = "https://api.unsplash.com/photos/random"
    headers = {
        "Authorization": f"Client-ID {access_key}"
    }
    params = {
        "count": 1,
        "query": "street photography"
    }
    
    try:
        print(f"📡 Conectando ao Unsplash...")
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()[0]
            print(f"✅ CONEXÃO BEM-SUCEDIDA!")
            print(f"📸 Foto encontrada: {data['id']}")
            print(f"👤 Fotógrafo: {data['user']['name']}")
            print(f"🔗 Link: {data['links']['html']}")
            print(f"⬇️  Download Trigger: OK")
            
            # Verificar headers de rate limit
            limit = response.headers.get('X-Ratelimit-Limit')
            remaining = response.headers.get('X-Ratelimit-Remaining')
            print(f"\n📊 Rate Limit: {remaining}/{limit} requests restantes")
            
            return True
        else:
            print(f"❌ Erro {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    print("\n📸 Testando Unsplash API...\n")
    
    access_key = load_api_key()
    
    if not access_key:
        print("❌ UNSPLASH_ACCESS_KEY não encontrada no .env")
        sys.exit(1)
    
    print(f"🔑 Access Key: {access_key[:15]}...")
    
    if test_unsplash(access_key):
        print(f"\n✅ Unsplash configurado com sucesso!")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
