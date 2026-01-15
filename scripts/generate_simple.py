#!/usr/bin/env python3
"""
Gerador Simplificado - Abordagem Direta
"""

import os
import sys
import json
import csv
import requests
from pathlib import Path

def load_story_from_csv(story_id):
    """Carrega dados da história do CSV"""
    csv_path = Path(__file__).parent.parent / 'data' / 'historias_base.csv'
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['id'] == story_id:
                return row
    return None

def load_api_key():
    """Carrega API key"""
    env_path = Path(__file__).parent.parent / '.env'
    with open(env_path, 'r') as f:
        for line in f:
            if line.startswith('GOOGLE_AI_API_KEY='):
                return line.split('=', 1)[1].strip()
    return None

def generate_story(story_data, api_key):
    """Gera história via Gemini com prompt direto"""
    
    # Prompt DIRETO e CONCISO
    prompt = f"""Crie um roteiro para vídeo curto (YouTube Shorts/Reels) sobre população em situação de rua.

DADOS DA HISTÓRIA:
- Nome (fictício): {story_data['NOME_FICTICIO']}
- Local: {story_data['LOCAL_COMUM']}
- Conflito: {story_data['CONFLITO_PRINCIPAL']}
- Solução: {story_data['DICA_CAPACITACAO']}
- Tema: {story_data['tema_narrativo']}

REQUISITOS DO ROTEIRO:
1. Entre 1100-1300 caracteres (crucial para narração de 70s)
2. Estrutura: Gancho (3s) → Identificação → Conflito → Solução
3. Tom: Empático mas não vitimizador. Foco em sistemas,não pessoas.
4. Narrativa de Marshall Ganz: História do Eu → Nós → Agora
5. Incluir dados estatísticos se relevante
6. Terminar com informação prática (endereço/telefone)

PROIBIDO:
- Termos como "coitado", "mendigo", "vagabundo"
- Culpabilizar indivíduos
- Linguagem piedosa ou paternalista

FORMATO DE SAÍDA:
Apenas o texto do roteiro, SEM títulos ou marcações estruturais.
Escreva um texto contínuo e fluido, pronto para narração.

IMPORTANTE: O roteiro deve ter PELO MENOS 1100 caracteres. Não economize palavras.

ROTEIRO:"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "temperature": 1.0,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 8192,
            "stopSequences": []
        }
    }
    
    response = requests.post(url, json=payload, timeout=60)
    
    if response.status_code == 200:
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    else:
        raise Exception(f"API Error {response.status_code}: {response.text}")

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 generate_simple.py <story_id>")
        sys.exit(1)
    
    story_id = sys.argv[1]
    
    print(f"\n🎬 Gerando Roteiro Simplificado - História #{story_id}\n")
    
    # Carregar dados
    story_data = load_story_from_csv(story_id)
    if not story_data:
        print("❌ História não encontrada")
        sys.exit(1)
    
    api_key = load_api_key()
    if not api_key:
        print("❌ API key não encontrada")
        sys.exit(1)
    
    print(f"📝 História: {story_data['NOME_FICTICIO']} - {story_data['tema_narrativo']}")
    print(f"🤖 Gerando com Gemini 2.5 Flash...\n")
    
    try:
        roteiro = generate_story(story_data, api_key)
        
        print(f"✅ ROTEIRO GERADO ({len(roteiro)} caracteres):\n")
        print("=" * 70)
        print(roteiro)
        print("=" * 70)
        
        # Salvar
        output_dir = Path(__file__).parent.parent / 'output'
        tema_slug = story_data['tema_narrativo'].lower().replace(' ', '_').replace('(', '').replace(')', '')
        output_path = output_dir / f'roteiro_{story_id}_{tema_slug}.txt'
        
        output_path.write_text(roteiro, encoding='utf-8')
        print(f"\n💾 Salvo em: {output_path}")
        
        # Validar tamanho
        if len(roteiro) < 1100:
            print(f"\n⚠️  ATENÇÃO: Roteiro muito curto ({len(roteiro)} chars)")
            print(f"    Meta: 1100-1300 caracteres")
        elif len(roteiro) > 1300:
            print(f"\n⚠️  ATENÇÃO: Roteiro muito longo ({len(roteiro)} chars)")
            print(f"    Meta: 1100-1300 caracteres")
        else:
            print(f"\n✅ Tamanho perfeito: {len(roteiro)} caracteres")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
