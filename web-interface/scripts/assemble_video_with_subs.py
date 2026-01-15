#!/usr/bin/env python3
"""
Montagem Final com Legendas e Imagens Unsplash
"""

import os
import sys
import subprocess
from pathlib import Path

def get_audio_duration(audio_path):
    cmd = [
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration', 
        '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except:
        return 90.0

def assemble_video(story_id):
    project_root = Path(__file__).parent.parent
    output_dir = project_root / 'output'
    
    audio_path = output_dir / 'audio' / f'audio_{story_id}.mp3'
    images_dir = output_dir / 'images_unsplash'
    subs_path = output_dir / 'subtitles' / f'subs_{story_id}.srt'
    final_output = output_dir / 'final' / f'video_final_{story_id}_pro.mp4'
    
    if not audio_path.exists():
        print(f"❌ Áudio não encontrado: {audio_path}")
        return False
        
    images = sorted(list(images_dir.glob('scene_*.jpg')))
    if len(images) < 5:
        print(f"❌ Imagens insuficientes em {images_dir} ({len(images)} found)")
        return False
        
    print(f"🎬 Iniciando Montagem Pro - História #{story_id}")
    print(f"   🎵 Áudio: {audio_path.name}")
    print(f"   📸 Imagens: {len(images)} (Unsplash)")
    print(f"   📝 Legendas: {subs_path.name if subs_path.exists() else 'PENDENTE'}")
    
    duration = get_audio_duration(audio_path)
    image_duration = duration / len(images)
    print(f"   ⏱️  Duração: {duration:.1f}s")
    
    # Criar input.txt
    input_txt_path = output_dir / 'images_unsplash_list.txt'
    with open(input_txt_path, 'w') as f:
        for img in images:
            f.write(f"file '{img.absolute()}'\n")
            f.write(f"duration {image_duration}\n")
        f.write(f"file '{images[-1].absolute()}'\n")
        
    # Filtro de legenda (com escape de path para Windows/Linux safe)
    # FFmpeg requer escaping exótico para caminhos em filtros
    cmd = [
        'ffmpeg', '-y',
        '-f', 'concat', '-safe', '0', '-i', str(input_txt_path),
        '-i', str(audio_path)
    ]

    # Filtros de vídeo: Scale/Crop para 1080x1920 (Vertical) + Legendas (se houver)
    filters = []
    
    # Scale e Crop para preencher tela 9:16
    filters.append("scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920")
    
    # Filtro de Legendas (se arquivo existir)
    if subs_path.exists():
        subs_path_str = str(subs_path.absolute()).replace(":", "\\:").replace("'", "'\\\\''")
        filters.append(f"subtitles='{subs_path_str}':force_style='FontSize=20,FontName=Arial,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=3,Outline=2,Shadow=1,MarginV=30'")
    else:
        print("⚠️  Legendas não encontradas. Gerando apenas com vídeo.")

    # Montar string de filtros
    filter_complex = ",".join(filters)
    
    cmd = [
        'ffmpeg', '-y',
        '-f', 'concat', '-safe', '0', '-i', str(input_txt_path),
        '-i', str(audio_path),
        '-vf', filter_complex,
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
        '-c:a', 'aac', '-b:a', '192k',
        '-shortest',
        str(final_output)
    ]
    
    print("\n⚙️  Renderizando vídeo (pode demorar alguns segundos)...")
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"\n✅ VÍDEO PRO GERADO!")
        print(f"   📂 Output: {final_output}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro FFmpeg: {e.stderr.decode()}")
        return False

if __name__ == '__main__':
    story_id = sys.argv[1] if len(sys.argv) > 1 else "002"
    assemble_video(story_id)
