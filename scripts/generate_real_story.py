#!/usr/bin/env python3
"""
Gerador de Roteiro REAL usando Google AI (Gemini)
"""

import os
import sys
import json
import requests
from pathlib import Path

def load_api_key():
    """Carrega API key do .env"""
    env_path = Path(__file__).parent.parent / '.env'
    with open(env_path, 'r') as f:
        for line in f:
            if line.startswith('GOOGLE_AI_API_KEY='):
                return line.split('=', 1)[1].strip()
    return None

def load_prompt(story_id):
    """Carrega prompt gerado para uma história"""
    prompt_path = Path(__file__).parent.parent / 'output' / f'prompt_historia_{story_id}.txt'
    if not prompt_path.exists():
        return None
    return prompt_path.read_text(encoding='utf-8')

def generate_with_gemini(prompt, api_key):
    """Gera conteúdo usando Gemini 2.5 Flash"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "temperature": 0.9,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 2048,
        }
    }
    
    response = requests.post(url, json=payload, timeout=60)
    
    if response.status_code == 200:
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    else:
        raise Exception(f"API Error {response.status_code}: {response.text}")

def save_story(story_id, content, tema):
    """Salva história gerada"""
    output_dir = Path(__file__).parent.parent / 'output'
    tema_slug = tema.lower().replace(' ', '_').replace('(', '').replace(')', '')
    output_path = output_dir / f'historia_{story_id}_{tema_slug}_real.md'
    
    output_path.write_text(content, encoding='utf-8')
    return output_path

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 generate_real_story.py <story_id>")
        print("Exemplo: python3 generate_real_story.py 002")
        sys.exit(1)
    
    story_id = sys.argv[1]
    
    print(f"\n{'='*70}")
    print(f"🎬 GERANDO ROTEIRO REAL - História #{story_id}")
    print(f"{'='*70}\n")
    
    # Carregar API key
    print("🔑 Carregando API key...")
    api_key = load_api_key()
    if not api_key:
        print("❌ API key não encontrada no .env")
        sys.exit(1)
    print(f"✅ API key: {api_key[:25]}...")
    
    # Carregar prompt
    print(f"\n📝 Carregando prompt da história {story_id}...")
    prompt = load_prompt(story_id)
    if not prompt:
        print(f"❌ Prompt não encontrado. Execute primeiro:")
        print(f"   python3 scripts/story_generator.py generate {story_id}")
        sys.exit(1)
    print(f"✅ Prompt carregado ({len(prompt)} caracteres)")
    
    # Gerar com Gemini
    print(f"\n🤖 Enviando para Gemini 2.5 Flash...")
    print(f"   (isso pode levar 10-30 segundos)")
    
    try:
        content = generate_with_gemini(prompt, api_key)
        print(f"✅ Roteiro gerado! ({len(content)} caracteres)")
        
        # Salvar
        print(f"\n💾 Salvando roteiro...")
        # Extrair tema do CSV
        import csv
        csv_path = Path(__file__).parent.parent / 'data' / 'historias_base.csv'
        tema = "desconhecido"
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['id'] == story_id:
                    tema = row['tema_narrativo']
                    break
        
        output_path = save_story(story_id, content, tema)
        print(f"✅ Salvo em: {output_path}")
        
        # Preview
        print(f"\n{'='*70}")
        print(f"📄 PREVIEW (primeiros 500 caracteres):")
        print(f"{'='*70}\n")
        print(content[:500] + "...")
        
        print(f"\n{'='*70}")
        print(f"✅ SUCESSO! Próximo passo:")
        print(f"   python3 scripts/ethical_validator.py")
        print(f"{'='*70}\n")
        
    except Exception as e:
        print(f"❌ Erro ao gerar: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
