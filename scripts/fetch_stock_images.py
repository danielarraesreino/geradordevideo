#!/usr/bin/env python3
"""
Fetch Stock Images - Unsplash API
Analisa o roteiro com Gemini para extrair keywords e baixa imagens reais.
"""

import os
import sys
import json
import requests
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Carregar env
project_root = Path(__file__).parent.parent
load_dotenv(project_root / '.env')

def load_gemini_key():
    return os.getenv('GOOGLE_AI_API_KEY')

def load_unsplash_key():
    return os.getenv('UNSPLASH_ACCESS_KEY')

def get_visual_keywords(story_text, api_key):
    """Usa Gemini para extrair 5 termos de busca visual do roteiro"""
    import requests
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    prompt = f"""Analise o seguinte roteiro de vídeo sobre população de rua e extraia 5 termos de busca VISUAL para encontrar fotos no Unsplash.
    
    ROTEIRO:
    {story_text}
    
    REQUISITOS:
    - Retorne APENAS um JSON array de strings.
    - Cada string deve ser um termo de busca em INGLÊS (Unsplash funciona melhor em inglês).
    - Foque em: atmosfera urbana, detalhes (mãos, pés), arquitetura, objetos simbólicos.
    - Evite termos abstratos. Seja concreto.
    - Exemplo de output: ["worn shoes on concrete", "clenched weathered hands", "imposing bank building facade", "public service sign reception", "hopeful person holding card"]
    """
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2}
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            text = response.json()['candidates'][0]['content']['parts'][0]['text']
            # Limpar markdown se houver
            text = text.replace('```json', '').replace('```', '').strip()
            return json.loads(text)
        else:
            print(f"❌ Erro Gemini: {response.text}")
            return []
    except Exception as e:
        print(f"❌ Erro ao extrair keywords: {e}")
        return []

def search_and_download_image(query, index, output_dir, access_key):
    """Busca e baixa uma imagem do Unsplash"""
    search_url = "https://api.unsplash.com/search/photos"
    headers = {"Authorization": f"Client-ID {access_key}"}
    params = {
        "query": query,
        "per_page": 1,
        "orientation": "portrait" # Vertical para Reels/Shorts
    }
    
    print(f"   🔍 Buscando: '{query}'...")
    
    try:
        response = requests.get(search_url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data['total'] == 0:
                print(f"      ⚠️  Nenhuma imagem encontrada para '{query}'")
                return False
                
            photo = data['results'][0]
            download_url = photo['links']['download_location']
            
            # Trigger download event (Required by API)
            requests.get(download_url, headers=headers, params={"client_id": access_key})
            
            # Download actual image
            img_url = photo['urls']['regular']
            img_data = requests.get(img_url).content
            
            filename = f"scene_{index+1:02d}_{query.replace(' ', '_')}.jpg"
            output_path = output_dir / filename
            
            with open(output_path, 'wb') as f:
                f.write(img_data)
                
            print(f"      ✅ Baixado: {filename} (by {photo['user']['name']})")
            return output_path
        else:
            print(f"      ❌ Erro Unsplash: {response.text}")
            return False
            
    except Exception as e:
        print(f"      ❌ Erro download: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Fetch Stock Images")
    parser.add_argument("story_id", help="ID da história (ex: 002)")
    args = parser.parse_args()
    
    print(f"\n📸 BUSCANDO IMAGENS REAIS - História #{args.story_id}")
    
    # 1. Carregar chaves
    gemini_key = load_gemini_key()
    unsplash_key = load_unsplash_key()
    
    if not gemini_key or not unsplash_key:
        print("❌ Chaves de API faltando no .env")
        sys.exit(1)
        
    # 2. Ler roteiro
    script_path = project_root / 'output' / f'roteiro_{args.story_id}_exclusão_financeira.txt'
    # Fallback para tentar achar qualquer arquivo de roteiro com esse ID
    if not script_path.exists():
        files = list((project_root / 'output').glob(f'roteiro_{args.story_id}_*.txt'))
        if files:
            script_path = files[0]
        else:
            # Fallback para o markdown gerado pelo primeiro script
            files_md = list((project_root / 'output').glob(f'historia_{args.story_id}_*_real.md'))
            if files_md:
                script_path = files_md[0]
            else:
                print(f"❌ Roteiro não encontrado para ID {args.story_id}")
                sys.exit(1)
                
    print(f"📝 Roteiro: {script_path.name}")
    script_text = script_path.read_text(encoding='utf-8')
    
    # 3. Extrair keywords
    print("\n🧠 Analisando roteiro para extrair cenas...")
    keywords = get_visual_keywords(script_text, gemini_key)
    
    if not keywords:
        print("❌ Falha ao gerar keywords")
        sys.exit(1)
        
    print(f"📋 Cenas identificadas: {keywords}")
    
    # 4. Baixar imagens
    output_dir = project_root / 'output' / 'images_unsplash'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    downloaded = 0
    for i, query in enumerate(keywords):
        if search_and_download_image(query, i, output_dir, unsplash_key):
            downloaded += 1
            
    print(f"\n✅ Concluído: {downloaded}/{len(keywords)} imagens baixadas em {output_dir}")

if __name__ == '__main__':
    main()
