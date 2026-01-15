#!/usr/bin/env python3
"""
Story Generator - Pop Rua 2026
Gera novas histórias usando o master prompt e variáveis do CSV.
"""

import csv
import sys
from pathlib import Path
from typing import Dict, List


class StoryGenerator:
    """Gerador de histórias baseado em templates."""
    
    def __init__(self, master_prompt_path: Path, csv_path: Path):
        """
        Inicializa gerador.
        
        Args:
            master_prompt_path: Caminho para master_prompt_storytelling.txt
            csv_path: Caminho para historias_base.csv
        """
        self.master_prompt = master_prompt_path.read_text(encoding='utf-8')
        self.stories_data = self._load_csv(csv_path)
    
    def _load_csv(self, csv_path: Path) -> List[Dict]:
        """Carrega dados do CSV."""
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    
    def generate_prompt_for_story(self, story_id: str) -> str:
        """
        Gera prompt completo para IA criar história específica.
        
        Args:
            story_id: ID da história no CSV (ex: "001")
            
        Returns:
            Prompt formatado pronto para GPT-4
        """
        # Buscar dados da história
        story_data = next((s for s in self.stories_data if s['id'] == story_id), None)
        
        if not story_data:
            raise ValueError(f"História ID '{story_id}' não encontrada no CSV")
        
        # Montar prompt final
        prompt = f"""
{self.master_prompt}

═══════════════════════════════════════════════════════════════════════════════
TAREFA: GERAR HISTÓRIA
═══════════════════════════════════════════════════════════════════════════════

Com base no prompt de sistema acima, gere uma história usando as seguintes variáveis:

VARIÁVEIS:
• LOCAL_COMUM: {story_data['LOCAL_COMUM']}
• NOME_FICTICIO: {story_data['NOME_FICTICIO']}
• CONFLITO_PRINCIPAL: {story_data['CONFLITO_PRINCIPAL']}
• DICA_CAPACITACAO: {story_data['DICA_CAPACITACAO']}
• TEMA_NARRATIVO: {story_data['tema_narrativo']}

INSTRUÇÕES:
1. Siga rigorosamente a estrutura de 4 partes (Hook > Identificação > Conflito > Fechamento)
2. Integre Story of Self + Us + Now de Marshall Ganz
3. Mantenha densidade de ~1200 caracteres no roteiro principal
4. Crie 5 descrições visuais faceless cinematográficas
5. Forneça dica de capacitação concreta (endereço/telefone real ou plausível)

OUTPUT ESPERADO:
Use exatamente o formato do arquivo exemplo_terminal_onibus.md

═══════════════════════════════════════════════════════════════════════════════
"""
        return prompt.strip()
    
    def list_available_stories(self) -> None:
        """Lista todas as histórias disponíveis no CSV."""
        print(f"\n{'ID':<5} {'Local':<30} {'Tema':<30}")
        print("=" * 65)
        
        for story in self.stories_data:
            story_id = story['id']
            local = story['LOCAL_COMUM'][:28] + '..' if len(story['LOCAL_COMUM']) > 30 else story['LOCAL_COMUM']
            tema = story['tema_narrativo'][:28] + '..' if len(story['tema_narrativo']) > 30 else story['tema_narrativo']
            print(f"{story_id:<5} {local:<30} {tema:<30}")
        
        print(f"\nTotal: {len(self.stories_data)} histórias disponíveis\n")


def main():
    """Função principal - CLI para gerar prompts."""
    project_root = Path(__file__).parent.parent
    master_prompt_path = project_root / 'prompts' / 'master_prompt_storytelling.txt'
    csv_path = project_root / 'data' / 'historias_base.csv'
    
    if not master_prompt_path.exists():
        print(f"❌ Master prompt não encontrado: {master_prompt_path}")
        sys.exit(1)
    
    if not csv_path.exists():
        print(f"❌ CSV não encontrado: {csv_path}")
        sys.exit(1)
    
    generator = StoryGenerator(master_prompt_path, csv_path)
    
    # Parse argumentos
    if len(sys.argv) < 2:
        print("📖 Pop Rua 2026 - Story Generator\n")
        print("USO:")
        print("  python scripts/story_generator.py list              # Listar histórias")
        print("  python scripts/story_generator.py generate <ID>     # Gerar prompt para ID")
        print("\nEXEMPLO:")
        print("  python scripts/story_generator.py generate 002")
        print("  (copie o output e cole no GPT-4 ou cursor com o master prompt)")
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == 'list':
        generator.list_available_stories()
    
    elif command == 'generate':
        if len(sys.argv) < 3:
            print("❌ Erro: Especifique o ID da história")
            print("   Exemplo: python scripts/story_generator.py generate 002")
            sys.exit(1)
        
        story_id = sys.argv[2]
        
        try:
            prompt = generator.generate_prompt_for_story(story_id)
            
            # Salvar prompt em arquivo
            output_file = project_root / 'output' / f'prompt_historia_{story_id}.txt'
            output_file.write_text(prompt, encoding='utf-8')
            
            print(f"\n✅ Prompt gerado com sucesso!")
            print(f"📄 Salvo em: {output_file}")
            print(f"\n{'='*70}")
            print("PRÓXIMOS PASSOS:")
            print("1. Copie o conteúdo do arquivo gerado")
            print("2. Cole no GPT-4, Claude, ou qualquer LLM compatível")
            print("3. Revise o output gerado")
            print("4. Execute: python scripts/ethical_validator.py")
            print(f"{'='*70}\n")
            
        except ValueError as e:
            print(f"❌ Erro: {e}")
            sys.exit(1)
    
    else:
        print(f"❌ Comando desconhecido: {command}")
        print("   Use 'list' ou 'generate <ID>'")
        sys.exit(1)


if __name__ == '__main__':
    main()
