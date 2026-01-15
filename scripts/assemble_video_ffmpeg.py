#!/usr/bin/env python3
"""
Montagem Final de Vídeo com FFmpeg
Combina áudio e imagens geradas em um vídeo estilo slideshow narrativo.
"""

import os
import sys
import subprocess
from pathlib import Path

def get_audio_duration(audio_path):
    """Obtém duração do áudio usando ffprobe"""
    cmd = [
        'ffprobe', 
        '-v', 'error', 
        '-show_entries', 'format=duration', 
        '-of', 'default=noprint_wrappers=1:nokey=1', 
        str(audio_path)
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except Exception as e:
        print(f"⚠️  Não foi possível ler duração exata: {e}")
        return 90.0 # Fallback seguro

def assemble_video(story_id):
    project_root = Path(__file__).parent.parent
    output_dir = project_root / 'output'
    
    # Caminhos dos assets
    audio_path = output_dir / 'audio' / f'audio_{story_id}.mp3'
    images_dir = output_dir / 'images'
    final_output = output_dir / 'final' / f'video_final_{story_id}.mp4'
    
    # Garantir diretório final
    final_output.parent.mkdir(parents=True, exist_ok=True)
    
    # Verificar assets
    if not audio_path.exists():
        print(f"❌ Áudio não encontrado: {audio_path}")
        return False
        
    images = sorted(list(images_dir.glob('scene_*.png')))
    if len(images) < 5:
        print(f"❌ Imagens insuficientes encontradas em {images_dir} (Encontradas: {len(images)})")
        return False

    print(f"🎬 Iniciando montagem para História #{story_id}")
    print(f"   🎵 Áudio: {audio_path.name}")
    print(f"   🖼️  Imagens: {len(images)} cenas")

    # Calcular duração por imagem
    duration = get_audio_duration(audio_path)
    image_duration = duration / len(images)
    print(f"   ⏱️  Duração Total: {duration:.1f}s ({image_duration:.1f}s por imagem)")
    
    # Criar arquivo de input para o demuxer do ffmpeg
    # Formato:
    # file 'path/to/image1.png'
    # duration 5
    input_txt_path = output_dir / 'images_list.txt'
    with open(input_txt_path, 'w') as f:
        for img in images:
            f.write(f"file '{img.absolute()}'\n")
            f.write(f"duration {image_duration}\n")
        # Repetir a última imagem para garantir que o vídeo cubra todo o áudio se houver arredondamento
        f.write(f"file '{images[-1].absolute()}'\n") 
    
    # Comando FFmpeg
    # -f concat: usa o demuxer de concatenação
    # -i audio: input de áudio
    # -vf: escala para 1080x1920 (vertical) se necessário, ou mantém original
    # -c:v libx264: codec de vídeo compatível
    # -pix_fmt yuv420p: garante compatibilidade com players
    # -shortest: termina o vídeo quando o stream mais curto (áudio ou vídeo) acabar
    
    cmd = [
        'ffmpeg',
        '-y', # Overwrite
        '-f', 'concat',
        '-safe', '0',
        '-i', str(input_txt_path),
        '-i', str(audio_path),
        '-c:v', 'libx264',
        '-r', '30',
        '-pix_fmt', 'yuv420p',
        '-shortest',
        str(final_output)
    ]
    
    print("\n⚙️  Executando FFmpeg...")
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"\n✅ VÍDEO FINAL GERADO COM SUCESSO!")
        print(f"   📂 Output: {final_output}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro no FFmpeg:")
        print(e.stderr if e.stderr else "Erro desconhecido")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        story_id = "002" # Default
    else:
        story_id = sys.argv[1]
        
    assemble_video(story_id)
