#!/usr/bin/env python3
"""
Gerador Customizado - Baseado em Master Prompt (Texto Livre)
"""

import os
import sys
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

# Carregar env
project_root = Path(__file__).parent.parent
load_dotenv(project_root / '.env')

def load_api_key():
    return os.getenv('GOOGLE_AI_API_KEY')

def generate_story_custom(base_text, directives, api_key):
    """Gera roteiro com base em texto livre e diretrizes"""
    
    prompt = f"""ATUE COMO: Diretor de Criação Agêntico.
    
    MISSÃO: Escrever um ROTEIRO COMPLETO E DETALHADO para um vídeo de 90 segundos.
    
    TEXTO BASE (História do Eu):
    "{base_text}"
    
    DIRETRIZES ESTRUTURAIS (Viral ST + Marshall Ganz):
    1. GANCHO (0-10s): Comece com o impacto visual do exame amassado e a frase de efeito.
    2. DESENVOLVIMENTO (Eu -> Nós): Expanda a história do Rogério. Descreva a semana de angústia. Conecte isso ao conceito de APARTAÇÃO SOCIAL. Mostre como o sistema faz ele se sentir invisível.
    3. CLÍMAX & SOLUÇÃO (Agora): A virada racional que o protegeu. A importância do amor e da informação.
    4. CHAMADA PARA AÇÃO (CTA): Apresente o "Consultório na Rua" e a "RAPS" como soluções de acolhimento em Campinas.
    
    REQUISITOS CRÍTICOS:
    - O texto DEVE ter entre 1100 e 1300 caracteres. (Escreva parágrafos completos, não frases soltas).
    - Use linguagem falada, fluida e emotiva.
    - NÃO use: "mendigo", "coitado", "viciado". Use: "pessoa em situação de rua", "uso abusivo".
    
    SAÍDA ESPERADA:
    Apenas o texto corrido da narração, pronto para o locutor ler. Não inclua "Cena 1", "Câmera", etc. Apenas a fala.
    """

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2000,
        }
    }
    
    response = requests.post(url, json=payload, timeout=60)
    
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        raise Exception(f"API Error {response.status_code}: {response.text}")

def main():
    print(f"\n🎬 Processando Master Prompt - História #005 (Rogério)\n")
    
    api_key = load_api_key()
    if not api_key:
        print("❌ API key não encontrada")
        sys.exit(1)
        
    # Texto fornecido pelo usuário
    base_text = "O Rogério foi procurado pelas técnicas do posto de saúde... depois de uma semana de espera descobre que está com hepatite B, e nessa semana de medo usou muito. A maconha funciona como analgésico para a dor da fissura de usar crack... Tive uma resposta racional que afastou o meu amigo do uso e me protegeu. A conclusão é: Sem perspectiva complica, o amor é importante e a ignorância salva"
    
    directives = """
    - Hook (0-3s): Close-up em um resultado de exame amassado enquanto uma voz profunda diz: "O medo de um papel pode te jogar de volta pro inferno".
    - Desenvolvimento (Eu/Nós): Use a angústia da espera do Rogério para ilustrar a **apartação social**: o sentimento de ser um "não semelhante" no sistema de saúde.
    - Ação (Agora): Informe que em Campinas existe o **Consultório na Rua** e a rede **RAPS** (Rede de Atenção Psicossocial), focada em suporte sem julgamentos.
    """
    
    try:
        roteiro = generate_story_custom(base_text, directives, api_key)
        
        print(f"✅ ROTEIRO GERADO ({len(roteiro)} caracteres):\n")
        print("=" * 70)
        print(roteiro)
        print("=" * 70)
        
        # Salvar
        output_dir = Path(__file__).parent.parent / 'output'
        output_path = output_dir / f'roteiro_005_rogerio_saude.txt'
        
        output_path.write_text(roteiro, encoding='utf-8')
        print(f"\n💾 Salvo em: {output_path}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
