# Pop Rua 2026 - Sistema de Storytelling Social Automatizado

> **Audiovisual como Microscópio**: Transformando a invisibilidade em empatia através da narrativa pública estratégica.

## 🎯 Missão

Gerar roteiros de vídeos *faceless* de alto impacto para **desnaturalizar a barbárie** da situação de rua em "lugares comuns", utilizando técnicas avançadas de narrativa pública e tecnologias de automação de 2026.

---

## 📁 Estrutura do Projeto

```
vector-galaxy/
└── web-interface/
    ├── prompts/           # Prompts de sistema
    ├── data/              # CSV de histórias
    ├── output/            # Roteiros e assets gerados
    ├── scripts/           # Scripts de automação
    ├── app/               # Interface Next.js (App Router)
    └── components/        # Componentes do Studio
```

---

## 🧠 Fundamentos Teóricos

### 1. Modelo de Narrativa Pública (Marshall Ganz)

Cada história conecta três camadas:

- **História do Eu**: Trajetória individual digna e humanizada
- **História do Nós**: Reflexo de valores comunitários e falhas sistêmicas
- **História do Agora**: Chamada para ação e visão de saída plausível

### 2. Técnica de Retenção Viral (Viral ST)

Estrutura em 4 fases para engajamento máximo:

1. **Gancho (0-3s)**: Fato potente em lugar comum
2. **Identificação (3-15s)**: Conexão emocional universal
3. **Conflito (15-45s)**: Problema sistêmico apresentado com dignidade
4. **Fechamento (45-60s)**: Reflexão + orientação prática

---

## 🛠️ Stack Tecnológica (2026)

| Componente | Tecnologia | Função |
|------------|------------|--------|
| **Narração** | ElevenLabs | Vozes hiper-realistas (modelo "Narrative - Empathetic") |
| **Visual Faceless** | Mootion / Midjourney | Geração cinematográfica preservando identidade |
| **Dados** | CSV → JSON | Alimentação automatizada de variáveis narrativas |
| **IA Criativa** | GPT-4 + Master Prompt | Direção de criação estratégica |

---

## 📊 Variáveis de Automação

O sistema utiliza 4 variáveis principais alimentadas via `historias_base.csv`:

```csv
$LOCAL_COMUM          → Local urbano cotidiano (terminal, praça, etc.)
$NOME_FICTICIO        → Nome fictício preservando dignidade
$CONFLITO_PRINCIPAL   → Obstáculo sistêmico específico
$DICA_CAPACITACAO     → Orientação prática de saída (endereço/telefone)
```

**Exemplo de linha do CSV:**

```
001,Terminal de Ônibus Central,Carlos,Impossibilidade de conseguir emprego sem endereço fixo,Centro Pop - Rua XV 123,Burocracia Excludente
```

---

## 📝 Exemplo de Output

Veja o arquivo completo: [`exemplo_terminal_onibus.md`](./output/exemplo_terminal_onibus.md)

**Métricas da história exemplo:**
- ✅ **Densidade:** 1203 caracteres (meta: ~1200)
- ✅ **Tempo de narração:** 65-75 segundos
- ✅ **Estrutura Viral ST:** Implementada completamente
- ✅ **Narrativa Pública Ganz:** Self + Us + Now integrados
- ✅ **Ética:** Dignidade preservada, foco em sistemas

### Fragmento do Roteiro:

> *"Você está no terminal de ônibus agora. Olhe ao redor. Aquele homem ali, encostado na coluna, se chama Carlos. Ele acorda antes de você todo dia. Carlos tem quarenta e dois anos, formação técnica em eletrônica e quinze anos de experiência em manutenção. Mas Carlos não tem emprego. Não por falta de capacidade. Por falta de um endereço..."*

---

## 🎨 Especificações Visuais (Faceless)

Cada roteiro inclui 5 descrições detalhadas para geração visual:

**Exemplo - Cena de Abertura:**
```
Wide shot, terminal de ônibus às 6h da manhã, movimento acelerado 
de pessoas cruzando quadro, luz fria de néon refletindo no chão 
molhado, foco em uma coluna de concreto no centro
```

**Princípios:**
- Preservação de identidade (sem rostos)
- Foco em objetos, ambientes e detalhes universais
- Estética documentário cinematográfico
- Dignidade visual mantida

---

## ⚖️ Compromissos Éticos

1. **Desnaturalização, não vitimização**: Foco em sistemas que falharam, não em pessoas que falharam
2. **Dignidade acima de tudo**: Se a história não eleva, não é publicada
3. **Linguagem acessível, nunca simplória**: Evita jargões acadêmicos e pasteurização
4. **Agilização social**: Sempre oferece saída concreta e acionável
5. **Direitos humanos inegociáveis**: Moradia e alimentação como direitos, não favores

---

## 🚀 Próximos Passos (Roadmap)

### Fase 2: Automação
- [ ] Integrar API do ElevenLabs para narração automatizada
- [ ] Pipeline de geração visual com Mootion/Midjourney
- [ ] Sistema de validação ética por checklist automatizado
- [ ] Batch processing de múltiplas histórias via CSV

### Fase 3: Distribuição
- [ ] Publicação multi-plataforma (TikTok, Reels, Shorts)
- [ ] Métricas de impacto social (engajamento + conversões para serviços)
- [ ] Sistema de feedback comunitário
- [ ] A/B testing de ganchos e fechamentos

---

## 📖 Como Usar

### 1. Studio Pop Rua (Interface Visual)

O projeto agora conta com um **Studio de Edição** local completo.

```bash
# Servidor de API (Backend Python)
python3 api_server.py

# Servidor de Interface (Frontend Next.js)
cd web-interface
npm run dev
```

Acesse: `http://localhost:3000`

### 2. Deploy na Vercel

Para rodar a interface na Vercel:
1. Conecte este repositório no dashboard da Vercel.
2. Nas configurações do projeto, defina **Root Directory** como `web-interface`.
3. O build command será `npm run build` e o output directory será `.next`.

> [!NOTE]
> As funcionalidades de edição (salvar roteiro) dependem de acesso ao sistema de arquivos local. No deploy da Vercel, estas funções podem ser limitadas se não houver um banco de dados persistente configurado.

### 2. Revisar Output

Todos os roteiros gerados vão para `/output` com:
- Texto narrativo (1200 chars)
- Descrições visuais (5 cenas)
- Dica de capacitação (endereço/telefone)
- Análise técnica de densidade e ética

### 3. Validação Ética

Checklist obrigatório antes de publicação:
- ✅ Dignidade preservada?
- ✅ Foco em sistemas, não pessoas?
- ✅ Linguagem acessível sem pasteurização?
- ✅ Saída concreta oferecida?
- ✅ Sem estereótipos reproduzidos?

---

## 📚 Base de Dados Atual

**10 histórias mapeadas** cobrindo temas:

1. Burocracia Excludente
2. Exclusão Financeira
3. Vulnerabilidade Material
4. Invisibilidade Social
5. Saúde Negligenciada
6. Exclusão Digital
7. Violência Institucional
8. Fragmentação Familiar
9. Saúde Mental
10. Discriminação Trabalhista

---

## 🤝 Contribuindo

Este é um projeto de impacto social. Contribuições éticas são bem-vindas:

1. **Novos locais comuns**: Identifique lugares urbanos ainda não mapeados
2. **Validação técnica**: Revise densidade de caracteres e tempo de narração
3. **Consultoria social**: Verifique precisão de recursos/serviços citados
4. **Testes de empatia**: Valide se histórias geram conexão sem vitimização

---

## 📄 Licença

Este projeto é dedicado ao **domínio público**. A humanidade não cobra royalties.

---

## 📞 Contato

Para dúvidas, sugestões ou parcerias de impacto social, abra uma issue ou contribua diretamente.

**Lembrete Final:** *A invisibilidade é uma escolha. Sua. E minha.*
