# Design Doc: Pop Rua Vids Studio (SaaS Architecture)

## 1. Visão Geral
Transformar a coleção de scripts CLI em uma **Plataforma Web SaaS** ("Pop Rua Studio") que permite:
- Gestão de Projetos (CRUD de Histórias)
- Editor de Roteiro Assistido por IA (Human-in-the-loop)
- Timeline de Assets (Drag & Drop de imagens/vídeos)
- Preview e Renderização na Nuvem

## 2. Arquitetura "State of the Art" (Híbrida)

Para manter a robustez dos scripts Python (Data Science/FFmpeg) com a interatividade moderna da Web, usaremos uma arquitetura **Monorepo**:

```text
/pop-rua-vids
├── apps
│   ├── web (Next.js 14 + Shadcn UI)       # Frontend Interativo (Editor, Dashboard)
│   └── api (FastAPI + Pydantic)           # Backend Robusto (Core Logic, FFmpeg)
├── packages
│   └── shared-types                       # Tipagem compartilhada (Single Source of Truth)
├── docker                                 # Containerização para Deploy
└── infrastructure                         # Terraform/Vercel config
```

## 3. Estratégias de Qualidade & Anti-Alucinação

Para garantir um código "perfeito, modular e escalável", implementaremos:

### A. Strict Typing (Contrato Rígido)
- **Frontend:** TypeScript (Zod para validação de forms).
- **Backend:** Python com Pydantic (Type Hints estritos).
- **Ponte:** Geração automática de cliente API (OpenAPI Generator) para garantir que o Front nunca chame algo que não existe no Back.

### B. Validation Layers (Anti-Alucinação)
Cada etapa do pipeline terá um "Guardrail" (Guardião):
1.  **Input Guard:** Validação de Schema (previne dados sujos entrarem).
2.  **Semantic Guard:** `ethical_validator.py` (já existente) rodando como middleware antes de permitir geração de áudio.
3.  **Output Guard:** Verificação automática de integridade de arquivos gerados (FFprobe) antes de devolver ao usuário.

### C. Modularidade (Hexagonal Architecture)
O Backend será dividido em domínios, não apenas funções:
- `modules/storytelling` (LLM logic)
- `modules/production` (FFmpeg, ElevenLabs)
- `modules/assets` (Unsplash, Uploads)

---

## 4. UI/UX: O "Editor Studio"

A interface terá 3 painéis principais:

1.  **O Roteirista (Esquerda):**
    - Editor de texto rico para o roteiro.
    - Botão "Validar Ética" em tempo real.
    - Destaque de sintaxe para "Hook", "Desenvolvimento", "Call to Action".

2.  **O Diretor (Centro/Direita):**
    - **Visualizador de Cenas:** Card para cada parágrafo do roteiro.
    - **Seletor de Imagem:** Busca Unsplash integrada ou Upload.
    - **Player de Áudio:** Preview da narração por bloco.

3.  **A Timeline (Inferior):**
    - Ajuste fino de duração.
    - Editor de Legendas (corrigir o que o Whisper gerou).

---

## 5. Próximos Passos (Plano de Migração)

1.  **Setup do Monorepo:** Iniciar Next.js e FastAPI.
2.  **Migração de Lógica:** Refatorar `scripts/*.py` para `apps/api/routers/*`.
3.  **Construção do Editor:** Criar a UI em React.
4.  **Integração:** Conectar os pontos.
