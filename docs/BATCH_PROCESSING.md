# Guia de Batch Processing - Pop Rua 2026

## 🚀 Processamento Automatizado em Lote

O sistema de batch processing permite gerar prompts para múltiplas histórias de forma automatizada, preparando-as para processamento via LLM (GPT-4, Claude, etc.).

---

## Comandos Disponíveis

### 1. Processar Todas as Histórias

```bash
python3 scripts/batch_processor.py
```

Gera prompts para todas as 16 histórias do CSV.

---

### 2. Processar Primeiras N Histórias

```bash
python3 scripts/batch_processor.py --limit 10
```

Processa apenas as primeiras 10 histórias (útil para testes).

---

### 3. Processar IDs Específicos

```bash
python3 scripts/batch_processor.py --ids 001 002 011 012
```

Gera prompts apenas para histórias específicas.

---

### 4. Forçar Regeração

```bash
python3 scripts/batch_processor.py --force
```

Regera prompts mesmo que já existam (sobrescreve).

---

## Workflow Completo

### Fase 1: Geração de Prompts (Automatizada)

```bash
# Gerar prompts para todas as histórias
python3 scripts/batch_processor.py

# Output:
# - output/prompt_historia_001.txt
# - output/prompt_historia_002.txt
# - ...
# - output/prompt_historia_016.txt
# - output/batch_report_<timestamp>.md
```

**Tempo estimado:** ~5 segundos para 16 histórias

---

### Fase 2: Processamento via LLM (Manual ou API)

**Opção A - Manual (Atual):**

1. Abrir `output/prompt_historia_001.txt`
2. Copiar conteúdo completo
3. Colar no GPT-4/Claude
4. Salvar resposta como `output/historia_001_burocracia_excludente.md`
5. Repetir para cada história

**Opção B - API (Futuro - Fase 2C):**

```python
# TODO: Implementar integração OpenAI/Anthropic
# scripts/llm_processor.py
# Lê todos os prompts e gera scripts automaticamente
```

---

### Fase 3: Validação Automática

```bash
python3 scripts/ethical_validator.py

# Output:
# 📄 historia_001_burocracia_excludente.md
#    ✅ APROVADO | Score: 86/100
# 
# 📄 historia_011_apartacao_social.md
#    ✅ APROVADO | Score: 79/100
#
# RESUMO: 14/16 histórias aprovadas
```

---

### Fase 4: Refinamento

Histórias com score < 70 precisam de ajustes:

```bash
# Ver recomendações específicas no output do validator
# Editar manualmente ou regerar via LLM com feedback
```

---

## Relatório de Batch

Após cada execução, um relatório é gerado:

**Arquivo:** `output/batch_report_<timestamp>.md`

### Exemplo de Conteúdo:

```markdown
# Batch Processing Report - Pop Rua 2026

**Data:** 2026-01-15 14:50:00

## Resumo Geral

- Total processado: 16
- Prompts gerados: 14
- Pulados (já existentes): 2
- Tempo total: 4.52s

## Detalhes por História

| ID | Tema | Status | Tempo |
|----|------|--------|-------|
| 001 | Burocracia Excludente | ⏭️ Pulado | 0.00s |
| 002 | Exclusão Financeira | ⏭️ Pulado | 0.00s |
| 003 | Vulnerabilidade Material | ✅ Gerado | 0.28s |
| ... | ... | ... | ... |

## Próximos Passos

1. Processar prompts gerados via GPT-4/Claude
2. Salvar outputs como `historia_XXX_tema.md`
3. Executar `python scripts/ethical_validator.py`
4. Refinar histórias com score < 70
```

**Também gerado:** `batch_report_<timestamp>.json` (dados estruturados)

---

## Prompts Especializados

O batch processor detecta automaticamente prompts especializados:

### Estrutura:

```
prompts/
├── master_prompt_storytelling.txt      # Prompt genérico (fallback)
├── prompt_apartacao_social.txt         # Especializado para Apartação Social
└── prompt_arquitetura_hostil.txt       # Especializado para Arquitetura Hostil
```

### Como Funciona:

1. Batch processor verifica se existe `prompt_{tema_slug}.txt`
2. Se existe: usa prompt especializado
3. Se não existe: usa master prompt genérico
4. Sempre injeta variáveis do CSV automaticamente

---

## Expansão para 50+ Histórias

### Passo 1: Adicionar ao CSV

Edite `data/historias_base.csv`:

```csv
017,Novo Local,Nome,Conflito,Dica,Tema,Eixo,Lei,Gancho
018,Outro Local,Nome2,Conflito2,Dica2,Tema2,B,Lei X,Dado Y
...
```

### Passo 2: Processar

```bash
python3 scripts/batch_processor.py --ids 017 018 019 020
```

### Passo 3: Validar

```bash
python3 scripts/ethical_validator.py
```

---

## Métricas de Qualidade

### Score Atual (3 histórias validadas):

| História | Score | Status |
|----------|-------|--------|
| Terminal Ônibus (#001) | 86/100 | ✅ Aprovado |
| Apartação Social (#011) | 79/100 | ✅ Aprovado |
| Arquitetura Hostil (#012) | 55/100 | ⚠️ Precisa ajuste |

**Média:** 73.3/100  
**Taxa de aprovação:** 66.7% (2/3)

### Meta para Produção:

- Score mínimo: 70/100
- Taxa de aprovação: >90%
- Densidade: 1100-1300 caracteres

---

## Troubleshooting

### Erro: "Master prompt não encontrado"

```bash
ls prompts/master_prompt_storytelling.txt
# Se não existir, verifique se está na pasta correta
```

### Erro: "CSV não encontrado"

```bash
ls data/historias_base.csv
# Verifique se o CSV está na pasta data/
```

### Prompts gerados mas não aparecem

```bash
ls -lh output/prompt_historia_*.txt
# Verificar se foram criados
```

---

## Roadmap de Automação

### ✅ Fase Atual: Semi-Automática

- Geração de prompts: ✅ Automatizada
- Processamento LLM: ⚠️ Manual
- Validação ética: ✅ Automatizada

### 🔄 Fase 2C: Totalmente Automática

```python
# Pipeline completo:
python3 scripts/full_automation.py --from-csv

# Fluxo:
# CSV → Prompts → GPT-4 API → Scripts → Validator → 
# → Aprovados → ElevenLabs → Mootion → FFmpeg → Video.mp4
```

---

## Performance

### Benchmarks (16 histórias):

- Geração de prompts: **~5 segundos**
- Processamento manual (GPT-4): **~15 min** (1 min/história)
- Validação: **~3 segundos**

### Com API (Estimado):

- Pipeline completo: **~30 minutos** (16 histórias)
- Custo estimado: **~$15** (GPT-4 + ElevenLabs + Midjourney)

---

## Arquivos Gerados

```
output/
├── prompt_historia_001.txt              # Prompts prontos para LLM
├── prompt_historia_002.txt
├── ...
├── historia_001_burocracia.md           # Scripts gerados
├── historia_011_apartacao_social.md
├── batch_report_1705337400.md           # Relatórios
└── batch_report_1705337400.json
```

---

**Última atualização:** 2026-01-15  
**Versão:** 2.0
