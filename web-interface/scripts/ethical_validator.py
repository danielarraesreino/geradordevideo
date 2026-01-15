#!/usr/bin/env python3
"""
Validador Ético - Pop Rua 2026
Verifica conformidade ética de roteiros gerados antes da publicação.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Resultado da validação ética."""
    approved: bool
    score: int  # 0-100
    issues: List[str]
    recommendations: List[str]
    metrics: Dict[str, any]


class EthicalValidator:
    """Validador de conformidade ética para histórias sociais."""
    
    # Termos que indicam vitimização (blacklist)
    VICTIMIZATION_TERMS = [
        r'\bcoitad[oa]s?\b',
        r'\bmendig[oa]s?\b',
        r'\bvagabund[oa]s?\b',
        r'\bpreguiços[oa]s?\b',
        r'\bsujos?\b',
        r'\bmargina(l|is)\b',
        r'\bcachaceir[oa]s?\b',
        r'\bbêbad[oa]s?\b',
    ]
    
    # Termos que indicam dignidade (whitelist - bônus)
    DIGNITY_TERMS = [
        r'\bdignidade\b',
        r'\bdireitos?\b',
        r'\bhumani(dade|zar|zação)\b',
        r'\brespeito\b',
        r'\bempoderamento\b',
    ]
    
    # Estrutura Viral ST esperada (keywords por seção)
    VIRAL_ST_STRUCTURE = {
        'hook': ['você', 'olhe', 'imagine', 'pense', 'repare'],
        'identification': ['se', 'nós', 'nosso', 'todo dia', 'também'],
        'conflict': ['mas', 'porém', 'sistema', 'impossível', 'armadilha'],
        'closure': ['existe', 'saída', 'pode', 'direito', 'agora']
    }
    
    def __init__(self, min_chars: int = 1100, max_chars: int = 1300):
        """
        Inicializa validador.
        
        Args:
            min_chars: Mínimo de caracteres aceito
            max_chars: Máximo de caracteres aceito
        """
        self.min_chars = min_chars
        self.max_chars = max_chars
    
    def validate_story(self, story_text: str, metadata: Dict = None) -> ValidationResult:
        """
        Valida uma história completa.
        
        Args:
            story_text: Texto do roteiro
            metadata: Metadados opcionais (local, nome, conflito, dica)
            
        Returns:
            ValidationResult com aprovação e detalhes
        """
        issues = []
        recommendations = []
        score = 100
        metrics = {}
        
        # 1. Validar densidade de caracteres
        char_count = len(story_text)
        metrics['char_count'] = char_count
        
        if char_count < self.min_chars:
            issues.append(f"Texto muito curto: {char_count} chars (mínimo: {self.min_chars})")
            score -= 20
            recommendations.append("Expandir narrativa com mais detalhes emocionais ou contexto")
        elif char_count > self.max_chars:
            issues.append(f"Texto muito longo: {char_count} chars (máximo: {self.max_chars})")
            score -= 10
            recommendations.append("Condensar sem perder profundidade emocional")
        
        # 2. Verificar termos de vitimização (CRÍTICO)
        victimization_found = []
        for pattern in self.VICTIMIZATION_TERMS:
            matches = re.findall(pattern, story_text, re.IGNORECASE)
            if matches:
                victimization_found.extend(matches)
        
        if victimization_found:
            issues.append(f"⚠️ CRÍTICO: Termos vitimizadores detectados: {', '.join(set(victimization_found))}")
            score -= 50  # Penalidade severa
            recommendations.append("Reescrever eliminando linguagem que desrespeita dignidade")
        
        metrics['victimization_terms'] = len(victimization_found)
        
        # 3. Verificar termos de dignidade (bônus)
        dignity_count = 0
        for pattern in self.DIGNITY_TERMS:
            dignity_count += len(re.findall(pattern, story_text, re.IGNORECASE))
        
        metrics['dignity_terms'] = dignity_count
        if dignity_count < 2:
            recommendations.append("Considere reforçar linguagem de dignidade e direitos")
            score -= 5
        
        # 4. Validar estrutura Viral ST
        st_score, st_issues = self._validate_viral_st(story_text)
        issues.extend(st_issues)
        score += st_score  # Pode adicionar ou subtrair
        metrics['viral_st_score'] = st_score
        
        # 5. Verificar presença de saída concreta (endereço/telefone)
        has_contact = bool(re.search(r'(\d{4,5}[-\s]?\d{4}|\bRua\b.*\d+|Tel:|Telefone)', story_text))
        has_address = bool(re.search(r'\bRua\b.*\d+', story_text))
        
        metrics['has_contact_info'] = has_contact
        metrics['has_address'] = has_address
        
        if not (has_contact or has_address):
            issues.append("Falta informação de contato concreta (endereço ou telefone)")
            score -= 25
            recommendations.append("Adicionar endereço e/ou telefone de serviço real na conclusão")
        
        # 6. Readability (Flesch Reading Ease aproximado)
        readability = self._estimate_readability(story_text)
        metrics['readability_score'] = readability
        
        if readability < 50:
            recommendations.append("Texto pode estar muito complexo - simplificar frases longas")
            score -= 5
        
        # 7. Determinar aprovação
        approved = score >= 70 and len(victimization_found) == 0
        
        if not approved and score >= 70:
            issues.append("História reprovada por termos vitimizadores, mesmo com score alto")
        
        return ValidationResult(
            approved=approved,
            score=max(0, min(100, score)),
            issues=issues,
            recommendations=recommendations,
            metrics=metrics
        )
    
    def _validate_viral_st(self, text: str) -> Tuple[int, List[str]]:
        """
        Valida estrutura Viral ST (Hook > Identificação > Conflito > Fechamento).
        
        Returns:
            (score_adjustment, issues)
        """
        issues = []
        score_adj = 0
        
        # Dividir texto em quartos aproximados
        length = len(text)
        sections = {
            'hook': text[:length//4],
            'identification': text[length//4:length//2],
            'conflict': text[length//2:3*length//4],
            'closure': text[3*length//4:]
        }
        
        # Verificar presença de keywords em cada seção
        for section_name, keywords in self.VIRAL_ST_STRUCTURE.items():
            section_text = sections[section_name].lower()
            found = sum(1 for kw in keywords if kw in section_text)
            
            if found == 0:
                issues.append(f"Seção '{section_name}' pode estar fraca - nenhuma keyword encontrada")
                score_adj -= 5
            elif found >= 2:
                score_adj += 2  # Bônus por boa estrutura
        
        return score_adj, issues
    
    def _estimate_readability(self, text: str) -> float:
        """
        Estima Flesch Reading Ease de forma aproximada.
        Score > 60 = fácil de ler
        """
        sentences = len(re.split(r'[.!?]+', text))
        words = len(text.split())
        syllables = sum(self._count_syllables(word) for word in text.split())
        
        if sentences == 0 or words == 0:
            return 0
        
        # Fórmula Flesch simplificada
        return 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
    
    def _count_syllables(self, word: str) -> int:
        """Conta sílabas de forma aproximada (heurística)."""
        word = word.lower()
        vowels = 'aeiouáéíóúâêôãõ'
        syllables = 0
        prev_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_was_vowel:
                syllables += 1
            prev_was_vowel = is_vowel
        
        return max(1, syllables)


def validate_markdown_file(filepath: Path) -> ValidationResult:
    """
    Valida arquivo markdown de roteiro.
    
    Args:
        filepath: Caminho para arquivo .md
        
    Returns:
        ValidationResult
    """
    content = filepath.read_text(encoding='utf-8')
    
    # Extrair apenas o roteiro (entre ## ROTEIRO e ## VISUAL)
    match = re.search(r'## ROTEIRO.*?\n\n(.*?)\n\n##', content, re.DOTALL)
    if not match:
        return ValidationResult(
            approved=False,
            score=0,
            issues=["Formato inválido: seção ROTEIRO não encontrada"],
            recommendations=["Verificar estrutura do arquivo"],
            metrics={}
        )
    
    story_text = match.group(1).strip()
    
    validator = EthicalValidator()
    return validator.validate_story(story_text)


def main():
    """Função principal - valida todos os arquivos em /output."""
    import sys
    
    output_dir = Path(__file__).parent.parent / 'output'
    
    if not output_dir.exists():
        print("❌ Diretório /output não encontrado")
        sys.exit(1)
    
    markdown_files = list(output_dir.glob('*.md'))
    
    if not markdown_files:
        print("⚠️  Nenhum arquivo .md encontrado em /output")
        sys.exit(0)
    
    print(f"🔍 Validando {len(markdown_files)} arquivo(s)...\n")
    
    results = []
    for filepath in markdown_files:
        print(f"📄 {filepath.name}")
        result = validate_markdown_file(filepath)
        results.append((filepath.name, result))
        
        # Exibir resultado
        status = "✅ APROVADO" if result.approved else "❌ REPROVADO"
        print(f"   {status} | Score: {result.score}/100")
        
        if result.issues:
            print("   Issues:")
            for issue in result.issues:
                print(f"     • {issue}")
        
        if result.recommendations:
            print("   Recomendações:")
            for rec in result.recommendations:
                print(f"     → {rec}")
        
        print(f"   Métricas: {json.dumps(result.metrics, indent=2)}")
        print()
    
    # Resumo final
    approved_count = sum(1 for _, r in results if r.approved)
    print(f"\n{'='*60}")
    print(f"RESUMO: {approved_count}/{len(results)} histórias aprovadas")
    print(f"{'='*60}")
    
    # Exit code para CI/CD
    sys.exit(0 if approved_count == len(results) else 1)


if __name__ == '__main__':
    main()
