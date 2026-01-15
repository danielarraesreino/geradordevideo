#!/usr/bin/env python3
"""
Orchestrator - Pop Rua 2026
Pipeline completo automatizado de geração de vídeos.

Executa os 5 passos:
1. Geração de Roteiro (Story Generator)
2. Validação Ética (Ethical Validator)
3. Narração (ElevenLabs API)
4. Visual (Mootion API)
5. Montagem Final (FFmpeg)
"""

import sys
import json
import time
import subprocess
from pathlib import Path
from typing import Dict, Optional, Tuple
from dataclasses import dataclass, asdict
import csv


@dataclass
class PipelineResult:
    """Resultado do pipeline completo."""
    story_id: str
    success: bool
    step_completed: int  # 1-5
    script_score: Optional[int]
    audio_path: Optional[str]
    video_path: Optional[str]
    final_video_path: Optional[str]
    errors: list
    total_time: float


class VideoOrchestrator:
    """Orquestrador de pipeline de vídeo."""
    
    def __init__(self, project_root: Path, api_keys: Dict[str, str], simulation_mode: bool = True):
        """
        Inicializa orquestrador.
        
        Args:
            project_root: Raiz do projeto
            api_keys: Dicionário com chaves de API
            simulation_mode: Se True, simula APIs sem fazer chamadas reais
        """
        self.project_root = project_root
        self.api_keys = api_keys
        self.simulation_mode = simulation_mode
        
        self.scripts_dir = project_root / 'scripts'
        self.output_dir = project_root / 'output'
        self.data_dir = project_root / 'data'
        
        # Criar diretórios se não existirem
        (self.output_dir / 'audio').mkdir(parents=True, exist_ok=True)
        (self.output_dir / 'video').mkdir(parents=True, exist_ok=True)
        (self.output_dir / 'final').mkdir(parents=True, exist_ok=True)
    
    def execute_pipeline(self, story_id: str) -> PipelineResult:
        """
        Executa pipeline completo para uma história.
        
        Args:
            story_id: ID da história (ex: '002')
            
        Returns:
            PipelineResult com status completo
        """
        print(f"\n{'='*80}")
        print(f"🎬 INICIANDO PIPELINE - História #{story_id}")
        print(f"{'='*80}\n")
        
        start_time = time.time()
        errors = []
        step = 0
        
        # Carregar dados da história
        story_data = self._load_story_data(story_id)
        if not story_data:
            return PipelineResult(
                story_id=story_id,
                success=False,
                step_completed=0,
                script_score=None,
                audio_path=None,
                video_path=None,
                final_video_path=None,
                errors=["História não encontrada no CSV"],
                total_time=time.time() - start_time
            )
        
        # PASSO 1: Geração de Roteiro
        print("📝 PASSO 1/5: Geração de Roteiro (Diretor de Criação)")
        script_path, script_success = self._step1_generate_script(story_id, story_data)
        if not script_success:
            errors.append("Falha na geração de roteiro")
            return self._create_result(story_id, 1, None, None, None, None, errors, start_time)
        
        step = 1
        print(f"   ✅ Roteiro gerado: {script_path}\n")
        
        # PASSO 2: Validação Ética
        print("⚖️  PASSO 2/5: Validação Ética (Auditor de Direitos)")
        score, validation_success = self._step2_validate_ethics(script_path)
        if not validation_success or score < 70:
            errors.append(f"Validação falhou (Score: {score}/100)")
            # TODO: Implementar reescrita automática
            return self._create_result(story_id, 2, score, None, None, None, errors, start_time)
        
        step = 2
        print(f"   ✅ Validação aprovada: {score}/100\n")
        
        # PASSO 3: Narração
        print("🎙️  PASSO 3/5: Narração Emotiva (ElevenLabs)")
        audio_path, audio_success = self._step3_generate_audio(script_path, story_id)
        if not audio_success:
            errors.append("Falha na geração de áudio")
            return self._create_result(story_id, 3, score, None, None, None, errors, start_time)
        
        step = 3
        print(f"   ✅ Áudio gerado: {audio_path}\n")
        
        # PASSO 4: Visual Cinematográfico
        print("🎥 PASSO 4/5: Produção Visual (Mootion Film Maker)")
        video_path, video_success = self._step4_generate_visuals(script_path, story_id)
        if not video_success:
            errors.append("Falha na geração de visual")
            return self._create_result(story_id, 4, score, audio_path, None, None, errors, start_time)
        
        step = 4
        print(f"   ✅ Visual gerado: {video_path}\n")
        
        # PASSO 5: Montagem Final
        print("🎬 PASSO 5/5: Montagem e Assembleia (FFmpeg)")
        final_path, montage_success = self._step5_final_montage(audio_path, video_path, story_id, script_path)
        if not montage_success:
            errors.append("Falha na montagem final")
            return self._create_result(story_id, 5, score, audio_path, video_path, None, errors, start_time)
        
        step = 5
        print(f"   ✅ Vídeo final: {final_path}\n")
        
        total_time = time.time() - start_time
        
        print(f"\n{'='*80}")
        print(f"✅ PIPELINE CONCLUÍDO - {total_time:.2f}s")
        print(f"{'='*80}\n")
        
        return PipelineResult(
            story_id=story_id,
            success=True,
            step_completed=5,
            script_score=score,
            audio_path=str(audio_path),
            video_path=str(video_path),
            final_video_path=str(final_path),
            errors=errors,
            total_time=total_time
        )
    
    def _load_story_data(self, story_id: str) -> Optional[Dict]:
        """Carrega dados da história do CSV."""
        csv_path = self.data_dir / 'historias_base.csv'
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['id'] == story_id:
                    return row
        return None
    
    def _step1_generate_script(self, story_id: str, story_data: Dict) -> Tuple[Path, bool]:
        """Passo 1: Gera roteiro usando story_generator.py."""
        try:
            # Executar story_generator.py
            result = subprocess.run(
                ['python3', str(self.scripts_dir / 'story_generator.py'), 'generate', story_id],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                print(f"   ❌ Erro: {result.stderr}")
                return None, False
            
            # Verificar se o prompt foi gerado
            prompt_path = self.output_dir / f'prompt_historia_{story_id}.txt'
            if not prompt_path.exists():
                return None, False
            
            # Em modo simulação, criar script fake
            if self.simulation_mode:
                script_path = self.output_dir / f'historia_{story_id}_{story_data["tema_narrativo"].lower().replace(" ", "_")}.md'
                
                # Simular conteúdo (em produção, isso viria do GPT-4/Claude)
                script_content = self._generate_mock_script(story_data)
                script_path.write_text(script_content, encoding='utf-8')
                
                time.sleep(0.5)  # Simular tempo de processamento
                return script_path, True
            
            else:
                # TODO: Integração real com GPT-4/Claude API
                print("   ⚠️  API não configurada - modo manual requerido")
                return None, False
                
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            return None, False
    
    def _step2_validate_ethics(self, script_path: Path) -> Tuple[int, bool]:
        """Passo 2: Valida ética usando ethical_validator.py."""
        try:
            # Em produção, executaria o validator
            if self.simulation_mode:
                time.sleep(0.3)  # Simular validação
                # Simular score alto
                score = 85
                print(f"   📊 Score: {score}/100")
                print(f"   📊 Termos vitimizadores: 0")
                print(f"   📊 Densidade: 1215 chars")
                return score, score >= 70
            
            else:
                # Executar validator real
                result = subprocess.run(
                    ['python3', str(self.scripts_dir / 'ethical_validator.py')],
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                # Parsear output (simplificado)
                if "APROVADO" in result.stdout:
                    # Extrair score do output
                    import re
                    match = re.search(r'Score: (\d+)/100', result.stdout)
                    score = int(match.group(1)) if match else 0
                    return score, True
                else:
                    return 0, False
                    
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            return 0, False
    
    def _step3_generate_audio(self, script_path: Path, story_id: str) -> Tuple[Path, bool]:
        """Passo 3: Gera narração usando ElevenLabs API."""
        audio_path = self.output_dir / 'audio' / f'audio_{story_id}.mp3'
        
        try:
            if self.simulation_mode:
                time.sleep(1.5)  # Simular processamento ElevenLabs
                
                # Criar arquivo dummy
                audio_path.write_text("SIMULATED AUDIO FILE", encoding='utf-8')
                
                print(f"   🎙️  Voz: Rachel (Narrative - Empathetic)")
                print(f"   🎙️  Velocidade: 0.95x")
                print(f"   🎙️  Duração estimada: 68s")
                
                return audio_path, True
            
            else:
                # TODO: Integração real com ElevenLabs
                if 'ELEVENLABS_API_KEY' not in self.api_keys:
                    print("   ❌ ELEVENLABS_API_KEY não configurada")
                    return None, False
                
                # Código de integração real aqui
                # import elevenlabs
                # ...
                
                return None, False
                
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            return None, False
    
    def _step4_generate_visuals(self, script_path: Path, story_id: str) -> Tuple[Path, bool]:
        """Passo 4: Gera visual usando Mootion API."""
        video_path = self.output_dir / 'video' / f'visual_{story_id}.mp4'
        
        try:
            if self.simulation_mode:
                time.sleep(2.0)  # Simular Mootion (2 min em produção)
                
                # Criar arquivo dummy
                video_path.write_text("SIMULATED VIDEO FILE", encoding='utf-8')
                
                print(f"   🎥 Estilo: Cinematic documentary faceless")
                print(f"   🎥 Resolução: 1080x1920 (vertical)")
                print(f"   🎥 Cenas geradas: 5")
                print(f"   🎥 Duração: 70s")
                
                return video_path, True
            
            else:
                # TODO: Integração real com Mootion
                if 'MOOTION_API_KEY' not in self.api_keys:
                    print("   ❌ MOOTION_API_KEY não configurada")
                    return None, False
                
                # Código de integração real aqui
                return None, False
                
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            return None, False
    
    def _step5_final_montage(self, audio_path: Path, video_path: Path, story_id: str, script_path: Path) -> Tuple[Path, bool]:
        """Passo 5: Montagem final usando FFmpeg."""
        final_path = self.output_dir / 'final' / f'video_final_{story_id}.mp4'
        
        try:
            if self.simulation_mode:
                time.sleep(1.0)  # Simular FFmpeg
                
                # Criar arquivo dummy
                final_path.write_text("SIMULATED FINAL VIDEO", encoding='utf-8')
                
                print(f"   🎬 Áudio + Vídeo sincronizados")
                print(f"   🎬 Legendas automáticas: PT-BR")
                print(f"   🎬 Otimização: Reels/Shorts")
                print(f"   🎬 Tamanho: ~25MB")
                
                return final_path, True
            
            else:
                # FFmpeg command real
                ffmpeg_cmd = [
                    'ffmpeg',
                    '-i', str(video_path),
                    '-i', str(audio_path),
                    '-c:v', 'libx264',
                    '-c:a', 'aac',
                    '-strict', 'experimental',
                    '-b:a', '192k',
                    '-shortest',
                    str(final_path)
                ]
                
                result = subprocess.run(ffmpeg_cmd, capture_output=True, timeout=60)
                
                if result.returncode == 0 and final_path.exists():
                    return final_path, True
                else:
                    print(f"   ❌ FFmpeg falhou: {result.stderr}")
                    return None, False
                    
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            return None, False
    
    def _generate_mock_script(self, story_data: Dict) -> str:
        """Gera script simulado para modo de teste."""
        return f"""# História {story_data['id']}: {story_data['tema_narrativo']}

## ROTEIRO (1215 caracteres - SIMULADO)

[Este é um roteiro simulado para fins de teste do pipeline]

{story_data['NOME_FICTICIO']} está em {story_data['LOCAL_COMUM']} todo dia. 
Enfrenta {story_data['CONFLITO_PRINCIPAL']}.

[Texto completo seria gerado por GPT-4/Claude aqui]

## DICA DE CAPACITAÇÃO

{story_data['DICA_CAPACITACAO']}

---
**Gerado por:** Modo Simulação - Pipeline Orchestrator v2.0
"""
    
    def _create_result(self, story_id, step, score, audio, video, final, errors, start_time):
        """Helper para criar PipelineResult."""
        return PipelineResult(
            story_id=story_id,
            success=False,
            step_completed=step,
            script_score=score,
            audio_path=audio,
            video_path=video,
            final_video_path=final,
            errors=errors,
            total_time=time.time() - start_time
        )


def main():
    """Função principal - CLI."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Video Orchestrator - Pop Rua 2026')
    parser.add_argument('story_id', help='ID da história (ex: 002)')
    parser.add_argument('--simulation', action='store_true', default=True, help='Modo simulação (sem APIs reais)')
    parser.add_argument('--api-keys-file', help='Arquivo JSON com chaves de API')
    
    args = parser.parse_args()
    
    # Carregar API keys
    api_keys = {}
    if args.api_keys_file:
        with open(args.api_keys_file, 'r') as f:
            api_keys = json.load(f)
    
    # Executar pipeline
    project_root = Path(__file__).parent.parent
    orchestrator = VideoOrchestrator(project_root, api_keys, simulation_mode=args.simulation)
    
    result = orchestrator.execute_pipeline(args.story_id)
    
    # Salvar relatório
    report_path = project_root / 'output' / f'pipeline_report_{args.story_id}.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(asdict(result), f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 Relatório salvo: {report_path}")
    
    if result.success:
        print(f"\n🎉 SUCESSO! Vídeo final: {result.final_video_path}")
        sys.exit(0)
    else:
        print(f"\n❌ FALHA no passo {result.step_completed}/5")
        print(f"Erros: {result.errors}")
        sys.exit(1)


if __name__ == '__main__':
    main()
