# Guia de Setup: APIs Gratuitas para Produção

> **Contexto:** O projeto Pop Rua 2026 está pronto no modo simulação. Este guia mostra como ativar o modo produção **SEM GASTAR DINHEIRO**, usando tiers gratuitos e alternativas open-source.

---

## 🎯 Objetivo

Transformar o pipeline simulado em **produção real** usando apenas recursos gratuitos disponíveis em 2026.

---

## 📊 Status Atual

✅ **Simulação funcionando** - Pipeline completo em 5.37s  
⏸️ **Produção pendente** - Aguardando configuração de APIs

---

## 🆓 Alternativas Gratuitas por Componente

### 1. Geração de Roteiro (LLM)

#### Opção A: Google AI Studio (GRATUITO - Recomendado)

**Por que escolher:**
- ✅ Totalmente gratuito
- ✅ Gemini 1.5 Pro incluído
- ✅ 60 requisições/minuto
- ✅ Sem cartão de crédito necessário

**Como obter a chave:**

1. **Acesse:** https://aistudio.google.com/app/apikey
2. **Faça login** com sua conta Google
3. **Clique em** "Get API Key"
4. **Copie a chave** que aparece (formato: `AIzaSy...`)
5. **Cole no arquivo** `.env`:
   ```bash
   GOOGLE_AI_API_KEY=AIzaSy_sua_chave_aqui
   ```

**Limites gratuitos:**
- 60 requests/minuto
- 1500 requests/dia
- Suficiente para gerar **50 histórias/dia**

---

#### Opção B: Groq (GRATUITO - Ultra Rápido)

**Por que escolher:**
- ✅ LLMs gratuitos e rápidos
- ✅ Llama 3.1 70B disponível
- ✅ 30 req/min no tier gratuito

**Como obter:**

1. **Acesse:** https://console.groq.com/keys
2. **Crie conta** (email + senha)
3. **Gere API Key** no dashboard
4. **Cole no `.env`:**
   ```bash
   GROQ_API_KEY=gsk_sua_chave_aqui
   ```

---

#### Opção C: Hugging Face (GRATUITO - Open Source)

**Por que escolher:**
- ✅ 100% gratuito e open-source
- ✅ Modelos locais ou via API
- ✅ Sem limites de rate

**Como obter:**

1. **Acesse:** https://huggingface.co/settings/tokens
2. **Crie conta**
3. **Gere token** (tipo: Read)
4. **Cole no `.env`:**
   ```bash
   HUGGINGFACE_API_KEY=hf_sua_chave_aqui
   ```

**Modelos recomendados:**
- `mistralai/Mixtral-8x7B-Instruct-v0.1`
- `meta-llama/Meta-Llama-3-70B-Instruct`

---

### 2. Narração de Áudio

#### Opção A: ElevenLabs Free Tier (LIMITADO MAS GRATUITO)

**Limites:**
- ✅ 10.000 caracteres/mês grátis
- ✅ 3 vozes customizadas
- ✅ Qualidade alta

**Como fazer dar certo:**
- Cada roteiro = ~1200 chars
- 10.000 chars ÷ 1200 = **~8 vídeos/mês grátis**

**Como obter:**

1. **Acesse:** https://elevenlabs.io/sign-up
2. **Crie conta gratuita**
3. **Vá em Settings** > **API Keys**
4. **Copie a chave**
5. **Cole no `.env`:**
   ```bash
   ELEVENLABS_API_KEY=sk_sua_chave_aqui
   ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM
   ```

**Dica:** Use apenas para vídeos finais após validação.

---

#### Opção B: Coqui TTS (100% GRATUITO - Local)

**Por que escolher:**
- ✅ Totalmente gratuito
- ✅ Roda no seu computador
- ✅ Sem limites de uso
- ❌ Qualidade inferior ao ElevenLabs

**Como instalar:**

```bash
# Instalar Coqui TTS
pip install TTS

# Gerar áudio (exemplo)
tts --text "Seu roteiro aqui" \
    --model_name tts_models/pt/cv/vits \
    --out_path output/audio.wav
```

**Integração no projeto:**
- Arquivo: `scripts/tts_local.py` (a ser criado)
- Sem necessidade de API key

---

### 3. Visual Cinematográfico

#### Opção A: Leonardo.ai Free Tier (GRATUITO)

**Limites:**
- ✅ 150 tokens/dia grátis
- ✅ ~30 imagens/dia
- ✅ Qualidade profissional

**Como obter:**

1. **Acesse:** https://app.leonardo.ai/
2. **Crie conta** (Google OAuth recomendado)
3. **Vá em Settings** > **API Access**
4. **Gere API Key**
5. **Cole no `.env`:**
   ```bash
   LEONARDO_API_KEY=sua_chave_aqui
   ```

**Workflow:**
- Gerar 5 imagens por história
- Criar vídeo com transições no FFmpeg

---

#### Opção B: Stability AI Free Tier

**Limites:**
- ✅ 25 créditos/mês grátis
- ✅ Stable Diffusion 3

**Como obter:**

1. **Acesse:** https://platform.stability.ai/account/keys
2. **Crie conta**
3. **Copie API Key**
4. **Cole no `.env`:**
   ```bash
   STABILITY_API_KEY=sk-sua_chave_aqui
   ```

---

#### Opção C: ComfyUI (100% GRATUITO - Local)

**Por que escolher:**
- ✅ Totalmente gratuito
- ✅ Controle total
- ✅ Modelos open-source (SDXL)
- ❌ Requer GPU (mínimo 8GB VRAM)

**Instalação:**
```bash
# Clone ComfyUI
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI
pip install -r requirements.txt

# Baixar modelo
# Siga: https://github.com/comfyanonymous/ComfyUI#manual-install
```

**Uso:**
- Interface web local
- Gerar imagens via workflow
- Sem custo adicional

---

### 4. Montagem de Vídeo

#### FFmpeg (100% GRATUITO - Já disponível)

**Status:** ✅ Já instalado no Linux

**Verificar instalação:**
```bash
ffmpeg -version
```

**Se não instalado:**
```bash
sudo apt install ffmpeg  # Ubuntu/Debian
```

**Custo:** R$ 0,00 ✅

---

## 🎬 Configuração Recomendada (Custo Zero)

### Stack Ideal sem Gastar:

1. **LLM:** Google AI Studio (Gemini 1.5 Pro)
2. **Áudio:** Coqui TTS local + ElevenLabs (8 vídeos/mês)
3. **Visual:** Leonardo.ai (30 imagens/dia)
4. **Montagem:** FFmpeg (local)

### Capacidade:

- **Vídeos/dia:** ~5-6
- **Vídeos/mês:** ~150
- **Custo total:** R$ 0,00

---

## 📝 Passo a Passo: Ativando Modo Produção

### Passo 1: Criar arquivo `.env`

```bash
cd /home/dan/.gemini/antigravity/playground/vector-galaxy
cp .env.example .env
```

### Passo 2: Obter chaves (escolha 1 de cada categoria)

**LLM (escolha uma):**
- [ ] Google AI Studio → `GOOGLE_AI_API_KEY`
- [ ] Groq → `GROQ_API_KEY`
- [ ] Hugging Face → `HUGGINGFACE_API_KEY`

**Áudio (escolha uma):**
- [ ] ElevenLabs Free → `ELEVENLABS_API_KEY`
- [ ] Coqui TTS Local (sem chave)

**Visual (escolha uma):**
- [ ] Leonardo.ai → `LEONARDO_API_KEY`
- [ ] Stability AI → `STABILITY_API_KEY`
- [ ] ComfyUI Local (sem chave)

### Passo 3: Preencher `.env`

Exemplo mínimo:
```bash
# LLM
GOOGLE_AI_API_KEY=AIzaSy_sua_chave_google

# Áudio (opcional se usar Coqui local)
ELEVENLABS_API_KEY=sk_sua_chave_elevenlabs

# Visual
LEONARDO_API_KEY=sua_chave_leonardo

# Modo
SIMULATION_MODE=false
```

### Passo 4: Testar conexão

```bash
# Testar com história #002
python3 scripts/orchestrator.py 002
```

Se tudo funcionar, verá:
```
✅ PIPELINE CONCLUÍDO
🎉 SUCESSO! Vídeo final: output/final/video_final_002.mp4
```

---

## 🚨 Troubleshooting

### Erro: "API Key inválida"

**Solução:**
1. Verificar se copiou a chave completa
2. Verificar se não tem espaços extras
3. Recriar a chave no dashboard

### Erro: "Rate limit exceeded"

**Solução:**
1. Esperar 1 minuto (reset automático)
2. Usar alternativa (ex: trocar Google AI por Groq)
3. Processar em batches menores

### Erro: "FFmpeg não encontrado"

**Solução:**
```bash
sudo apt update
sudo apt install ffmpeg
```

---

## 💡 Estratégia de Produção Sustentável

### Fase 1: Protótipo (Mês 1)
- Usar 100% ferramentas gratuitas
- Gerar 10 vídeos de teste
- Validar qualidade com comunidade

### Fase 2: Validação (Mês 2-3)
- Usar ElevenLabs para 8 vídeos/mês (melhor qualidade)
- Completar com Coqui TTS local para outros
- Coletar métricas de engajamento

### Fase 3: Escala (Mês 4+)
- Se houver orçamento: migrar para planos pagos
- Se não: continuar com gratuitos + automação

---

## 📊 Comparativo de Qualidade

| Componente | Opção Paga | Opção Gratuita | Diferença |
|------------|------------|----------------|-----------|
| **LLM** | GPT-4 | Gemini 1.5 Pro | Mínima |
| **Áudio** | ElevenLabs Pro | ElevenLabs Free | Apenas limite |
| **Visual** | Midjourney | Leonardo.ai | ~10% qualidade |
| **Montagem** | Premiere Pro | FFmpeg | Mesma qualidade |

**Conclusão:** É possível produzir conteúdo **85-90% da qualidade profissional** sem gastar nada.

---

## 🎯 Próximo Passo

**O que fazer agora:**

1. **Escolher stack gratuita** (recomendo: Google AI + Leonardo + ElevenLabs Free)
2. **Seguir "Passo a Passo" acima**
3. **Gerar primeiro vídeo real**
4. **Me mostrar para validarmos juntos**

**Quer que eu te oriente agora para criar a primeira chave?**

Podemos começar pela mais fácil: **Google AI Studio** (leva 2 minutos).

---

**Última atualização:** 2026-01-15  
**Status:** Pronto para produção gratuita ✅
