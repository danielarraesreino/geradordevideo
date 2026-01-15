#!/usr/bin/env python3
"""
Teste Google AI via HTTP direto (sem dependências problemáticas)
"""

import os
import json
import sys

# Carregar API key
env_path = '/home/dan/.gemini/antigravity/playground/vector-galaxy/.env'
api_key = None

with open(env_path, 'r') as f:
    for line in f:
        if line.startswith('GOOGLE_AI_API_KEY='):
            api_key = line.split('=', 1)[1].strip()
            break

if not api_key:
    print("❌ API key não encontrada")
    sys.exit(1)

print(f"✅ API Key: {api_key[:25]}...")

# Testar com requests
try:
    import requests
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": "Responda apenas: 'Conexão bem-sucedida com Google AI Studio!'"
            }]
        }]
    }
    
    print("\n📡 Testando conexão via HTTP...")
    
    response = requests.post(url, json=payload, timeout=30)
    
    if response.status_code == 200:
        data = response.json()
        text = data['candidates'][0]['content']['parts'][0]['text']
        
        print(f"\n🎉 SUCESSO TOTAL!")
        print(f"📝 Resposta do Gemini: {text}")
        print(f"\n✅ Google AI Studio FUNCIONANDO!")
        print(f"💡 Quota: 60 requisições/minuto")
        print(f"💡 Pronto para gerar roteiros reais!")
        
        sys.exit(0)
    else:
        print(f"❌ Erro HTTP {response.status_code}")
        print(f"   Resposta: {response.text[:200]}")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ Erro: {e}")
    sys.exit(1)
