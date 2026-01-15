#!/usr/bin/env python3
"""
Add Subtitles - Whisper (Local)
Gera legendas .srt sincronizadas para acessibilidade
"""

import os
import sys
import argparse
import whisper
import srt
import datetime
from pathlib import Path

def generate_subtitles(audio_path, output_path, model_size="base"):
    """Gera legendas usando Whisper"""
    print(f"🧠 Carregando modelo Whisper '{model_size}' (pode demorar no primeiro uso)...")
    
    try:
        model = whisper.load_model(model_size)
    except Exception as e:
        print(f"❌ Erro ao carregar Whisper: {e}")
        return False
        
    print(f"🎧 Transcrevendo áudio: {audio_path.name}...")
    
    # Transcrever
    result = model.transcribe(str(audio_path), language="pt")
    
    # Converter para SRT
    subtitles = []
    for i, segment in enumerate(result["segments"]):
        start = datetime.timedelta(seconds=segment["start"])
        end = datetime.timedelta(seconds=segment["end"])
        text = segment["text"].strip()
        
        subtitles.append(srt.Subtitle(index=i+1, start=start, end=end, content=text))
    
    # Salvar arquivo
    srt_content = srt.compose(subtitles)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(srt_content)
        
    print(f"✅ Legendas salvas em: {output_path}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Generate Subtitles with Whisper")
    parser.add_argument("story_id", help="ID da história (ex: 002)")
    parser.add_argument("--model", default="base", help="Modelo Whisper (tiny, base, small, medium, large)")
    args = parser.parse_args()
    
    project_root = Path(__file__).parent.parent
    audio_path = project_root / 'output' / 'audio' / f'audio_{args.story_id}.mp3'
    
    if not audio_path.exists():
        print(f"❌ Áudio não encontrado: {audio_path}")
        sys.exit(1)
        
    output_dir = project_root / 'output' / 'subtitles'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    srt_path = output_dir / f'subs_{args.story_id}.srt'
    
    print(f"\n📝 GERANDO LEGENDAS - História #{args.story_id}")
    
    if generate_subtitles(audio_path, srt_path, args.model):
        print(f"\n✅ Concluído com sucesso!")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
