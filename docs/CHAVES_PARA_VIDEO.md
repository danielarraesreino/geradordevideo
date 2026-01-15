# 🎬 Chaves Necessárias para Vídeo Final

## Status Atual:
- ✅ **Google AI Studio** - CONFIGURADO
- ⏳ **ElevenLabs** (Áudio) - PENDENTE
- ⏳ **Leonardo.ai** (Visual) - PENDENTE  
- ✅ **FFmpeg** (Montagem) - JÁ INSTALADO

---

## 🎙️ PASSO 1: ElevenLabs (Narração de Áudio)

### O que é:
Converte texto em voz ultra-realista, perfeita para narração emotiva.

### Tier Gratuito:
- ✅ **10.000 caracteres/mês** grátis
- ✅ ~**8 vídeos/mês** sem pagar nada
- ✅ Qualidade profissional

### Como obter (2 minutos):

1. **Acesse:** https://elevenlabs.io/sign-up
2. **Crie conta** (pode usar Google OAuth)
3. **Vá em:** Profile (canto superior direito) → API Keys
4. **Clique:** "Create API Key"
5. **Copie a chave** (começa com `sk_...`)
6. **Cole no .env:**
   ```
   ELEVENLABS_API_KEY=sk_sua_chave_aqui
   ```

### Voz Recomendada:
- **Rachel** (empática, feminina) - ID: `21m00Tcm4TlvDq8ikWAM`
- **Adam** (profunda, masculina) - ID: `pNInz6obpgDQGcFmaJgB`

---

## 🎨 PASSO 2: Leonardo.ai (Geração Visual)

### O que é:
Gera imagens cinematográficas faceless para os vídeos.

### Tier Gratuito:
- ✅ **150 tokens/dia** grátis
- ✅ ~**30 imagens/dia** (5 por vídeo = 6 vídeos/dia)
- ✅ Sem cartão de crédito necessário

### Como obter (3 minutos):

1. **Acesse:** https://app.leonardo.ai/
2. **Crie conta** (Google OAuth recomendado)
3. **Confirme email**
4. **Vá em:** User Settings (canto superior direito) → API Access
5. **Clique:** "Create API Key"
6. **Copie a chave**
7. **Cole no .env:**
   ```
   LEONARDO_API_KEY=sua_chave_aqui
   ```

---

## 🎬 ALTERNATIVA: Pipeline 100% Gratuito e Local

Se preferir **não depender de APIs externas**, podemos usar:

### Áudio:
- **Coqui TTS** (local, ilimitado, qualidade 80% do ElevenLabs)
  ```bash
  pip install TTS
  ```

### Visual:
- **ComfyUI + SDXL** (local, requer GPU 8GB+, qualidade profissional)
  - Mais demorado mas 100% offline

---

## 📊 Comparação de Custo:

| Pipeline | Custo/mês | Vídeos/mês | Qualidade |
|----------|-----------|------------|-----------|
| **Gratuito Cloud** | R$ 0 | ~8 | 95% |
| **Gratuito Local** | R$ 0 | Ilimitado | 80% |
| **Pago** | ~R$ 50 | Ilimitado | 100% |

---

## 🚀 PRÓXIMO PASSO RECOMENDADO:

**Para ver o vídeo final HOJE:**

1. **Crie conta ElevenLabs** (2 min) 
   - Link: https://elevenlabs.io/sign-up
   - Copie a API key

2. **Crie conta Leonardo.ai** (3 min)
   - Link: https://app.leonardo.ai/
   - Copie a API key

3. **Cole ambas no `.env`**

4. **Rode o pipeline automático:**
   ```bash
   python3 scripts/full_pipeline.py 002
   ```

**Resultado:** `video_final_002.mp4` em ~5 minutos

---

## ⚡ ATALHO RÁPIDO (Só áudio, sem visual):

Se quiser testar mais rápido, posso gerar apenas o áudio narrado agora:

```bash
# Só precisa da chave do ElevenLabs
python3 scripts/generate_audio.py 002
```

**Isso gera:** `audio_002.mp3` com narração profissional em 10 segundos.

---

**Qual você prefere?**

A) Configurar ElevenLabs + Leonardo agora (5 min total) → vídeo completo  
B) Só ElevenLabs agora → ouvir a narração primeiro  
C) Pipeline 100% local (mais demorado de configurar)

**Aguardando suas chaves ou preferência!** 🎯
