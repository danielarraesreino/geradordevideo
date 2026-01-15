#!/usr/bin/env python3
"""
Batch Story Processor - Pop Rua 2026
Processa múltiplas histórias do CSV em lote, validando cada uma.
"""

import csv
import json
import sys
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
import time


@dataclass
class BatchResult:
    """Resultado do processamento em lote."""
    story_id: str
    tema: str
    prompt_generated: bool
    script_path: Optional[str]
    validation_score: Optional[int]
    validation_approved: bool
    errors: List[str]
    processing_time: float


class BatchProcessor:
    """Processador em lote de histórias."""
    
    def __init__(self, project_root: Path):
        """
        Inicializa processador.
        
        Args:
            project_root: Raiz do projeto vector-galaxy
        """
        self.project_root = project_root
        self.csv_path = project_root / 'data' / 'historias_base.csv'
        self.output_dir = project_root / 'output'
        self.prompts_dir = project_root / 'prompts'
        
        # Carregar stories
        self.stories = self._load_stories()
    
    def _load_stories(self) -> List[Dict]:
        """Carrega histórias do CSV."""
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    
    def process_batch(
        self, 
        story_ids: Optional[List[str]] = None,
        limit: Optional[int] = None,
        skip_existing: bool = True
    ) -> List[BatchResult]:
        """
        Processa histórias em lote.
        
        Args:
            story_ids: IDs específicos (None = todos)
            limit: Limite de histórias a processar
            skip_existing: Pular histórias já geradas
            
        Returns:
            Lista de resultados
        """
        results = []
        
        # Filtrar histórias
        stories_to_process = self.stories
        if story_ids:
            stories_to_process = [s for s in self.stories if s['id'] in story_ids]
        
        if limit:
            stories_to_process = stories_to_process[:limit]
        
        print(f"\n{'='*70}")
        print(f"🚀 BATCH PROCESSING - {len(stories_to_process)} histórias")
        print(f"{'='*70}\n")
        
        for idx, story in enumerate(stories_to_process, 1):
            story_id = story['id']
            tema = story['tema_narrativo']
            
            print(f"[{idx}/{len(stories_to_process)}] Processando ID {story_id}: {tema}")
            
            start_time = time.time()
            errors = []
            
            # Verificar se já existe
            existing_scripts = list(self.output_dir.glob(f'historia_{story_id}_*.md'))
            if skip_existing and existing_scripts:
                print(f"  ⏭️  Pulando (já existe: {existing_scripts[0].name})")
                results.append(BatchResult(
                    story_id=story_id,
                    tema=tema,
                    prompt_generated=False,
                    script_path=str(existing_scripts[0]),
                    validation_score=None,
                    validation_approved=None,
                    errors=["Skipped - already exists"],
                    processing_time=0
                ))
                continue
            
            # 1. Gerar prompt
            prompt_path = self.output_dir / f'prompt_historia_{story_id}.txt'
            prompt_generated = self._generate_prompt(story_id, prompt_path)
            
            if not prompt_generated:
                errors.append("Falha ao gerar prompt")
            
            # Por enquanto, prompts precisam ser processados manualmente via LLM
            # TODO: Integração com OpenAI/Anthropic API para automação completa
            
            processing_time = time.time() - start_time
            
            result = BatchResult(
                story_id=story_id,
                tema=tema,
                prompt_generated=prompt_generated,
                script_path=str(prompt_path) if prompt_generated else None,
                validation_score=None,
                validation_approved=False,
                errors=errors,
                processing_time=processing_time
            )
            
            results.append(result)
            print(f"  ✅ Prompt gerado: {prompt_path.name}")
        
        return results
    
    def _generate_prompt(self, story_id: str, output_path: Path) -> bool:
        """
        Gera prompt para uma história.
        
        Args:
            story_id: ID da história
            output_path: Onde salvar o prompt
            
        Returns:
            True se gerado com sucesso
        """
        try:
            # Buscar dados da história
            story_data = next((s for s in self.stories if s['id'] == story_id), None)
            if not story_data:
                return False
            
            # Carregar master prompt
            master_prompt_path = self.prompts_dir / 'master_prompt_storytelling.txt'
            if not master_prompt_path.exists():
                return False
            
            master_prompt = master_prompt_path.read_text(encoding='utf-8')
            
            # Verificar se existe prompt especializado
            tema_slug = story_data['tema_narrativo'].lower().replace(' ', '_').replace('(', '').replace(')', '')
            specialized_prompt_path = self.prompts_dir / f'prompt_{tema_slug}.txt'
            
            if specialized_prompt_path.exists():
                # Usar prompt especializado
                specialized_prompt = specialized_prompt_path.read_text(encoding='utf-8')
                final_prompt = f"{specialized_prompt}\n\n{'='*80}\n\nVARIÁVEIS DA HISTÓRIA ID {story_id}:\n"
            else:
                # Usar master prompt genérico
                final_prompt = f"{master_prompt}\n\n{'='*80}\n\nTAREFA: GERAR HISTÓRIA\n{'='*80}\n\nCom base no prompt de sistema acima, gere uma história usando as seguintes variáveis:\n\nVARIÁVEIS:\n"
            
            # Adicionar variáveis
            final_prompt += f"• LOCAL_COMUM: {story_data['LOCAL_COMUM']}\n"
            final_prompt += f"• NOME_FICTICIO: {story_data['NOME_FICTICIO']}\n"
            final_prompt += f"• CONFLITO_PRINCIPAL: {story_data['CONFLITO_PRINCIPAL']}\n"
            final_prompt += f"• DICA_CAPACITACAO: {story_data['DICA_CAPACITACAO']}\n"
            final_prompt += f"• TEMA_NARRATIVO: {story_data['tema_narrativo']}\n"
            
            if 'eixo_canal' in story_data:
                final_prompt += f"• EIXO_CANAL: {story_data['eixo_canal']}\n"
            if 'lei_relevante' in story_data:
                final_prompt += f"• LEI_RELEVANTE: {story_data['lei_relevante']}\n"
            if 'gancho_estatistico' in story_data:
                final_prompt += f"• GANCHO_ESTATISTICO: {story_data['gancho_estatistico']}\n"
            
            final_prompt += f"\nINSTRUÇÕES:\n"
            final_prompt += f"1. Siga rigorosamente a estrutura de 4 partes (Hook > Identificação > Conflito > Fechamento)\n"
            final_prompt += f"2. Integre Story of Self + Us + Now de Marshall Ganz\n"
            final_prompt += f"3. Mantenha densidade de ~1200 caracteres no roteiro principal\n"
            final_prompt += f"4. Crie 5 descrições visuais faceless cinematográficas\n"
            final_prompt += f"5. Forneça dica de capacitação concreta (endereço/telefone real ou plausível)\n"
            
            if 'lei_relevante' in story_data and story_data['lei_relevante']:
                final_prompt += f"6. CITE obrigatoriamente: {story_data['lei_relevante']}\n"
            
            final_prompt += f"\nOUTPUT ESPERADO:\n"
            final_prompt += f"Use exatamente o formato do arquivo exemplo_terminal_onibus.md\n\n"
            final_prompt += f"{'='*80}\n"
            
            # Salvar
            output_path.write_text(final_prompt, encoding='utf-8')
            return True
            
        except Exception as e:
            print(f"  ❌ Erro ao gerar prompt: {e}")
            return False
    
    def generate_summary_report(self, results: List[BatchResult], output_path: Path):
        """
        Gera relatório resumido do batch.
        
        Args:
            results: Resultados do processamento
            output_path: Onde salvar o relatório
        """
        total = len(results)
        generated = sum(1 for r in results if r.prompt_generated)
        skipped = sum(1 for r in results if 'Skipped' in str(r.errors))
        
        report = f"# Batch Processing Report - Pop Rua 2026\n\n"
        report += f"**Data:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        report += f"## Resumo Geral\n\n"
        report += f"- Total processado: {total}\n"
        report += f"- Prompts gerados: {generated}\n"
        report += f"- Pulados (já existentes): {skipped}\n"
        report += f"- Tempo total: {sum(r.processing_time for r in results):.2f}s\n\n"
        
        report += f"## Detalhes por História\n\n"
        report += f"| ID | Tema | Status | Tempo |\n"
        report += f"|----|------|--------|-------|\n"
        
        for r in results:
            status = "✅ Gerado" if r.prompt_generated else "⏭️ Pulado"
            if r.errors and 'Skipped' not in str(r.errors):
                status = "❌ Erro"
            
            report += f"| {r.story_id} | {r.tema[:30]}... | {status} | {r.processing_time:.2f}s |\n"
        
        report += f"\n## Próximos Passos\n\n"
        report += f"1. Processar prompts gerados via GPT-4/Claude\n"
        report += f"2. Salvar outputs como `historia_XXX_tema.md`\n"
        report += f"3. Executar `python scripts/ethical_validator.py`\n"
        report += f"4. Refinar histórias com score < 70\n\n"
        
        # Salvar como JSON também
        json_path = output_path.with_suffix('.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump([asdict(r) for r in results], f, indent=2, ensure_ascii=False)
        
        output_path.write_text(report, encoding='utf-8')
        print(f"\n📊 Relatório salvo: {output_path}")
        print(f"📊 Dados JSON: {json_path}")


def main():
    """Função principal - CLI."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Batch Story Processor - Pop Rua 2026')
    parser.add_argument(
        '--ids', 
        nargs='+', 
        help='IDs específicos para processar (ex: 001 002 003)'
    )
    parser.add_argument(
        '--limit', 
        type=int, 
        help='Limite de histórias a processar'
    )
    parser.add_argument(
        '--force', 
        action='store_true',
        help='Regerar mesmo se já existir'
    )
    
    args = parser.parse_args()
    
    project_root = Path(__file__).parent.parent
    processor = BatchProcessor(project_root)
    
    # Processar
    results = processor.process_batch(
        story_ids=args.ids,
        limit=args.limit,
        skip_existing=not args.force
    )
    
    # Gerar relatório
    report_path = project_root / 'output' / f'batch_report_{int(time.time())}.md'
    processor.generate_summary_report(results, report_path)
    
    print(f"\n{'='*70}")
    print(f"✅ Batch processing concluído!")
    print(f"{'='*70}\n")


if __name__ == '__main__':
    main()
