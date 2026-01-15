# Guia: Unsplash API & Subtitles

Para evoluir o vídeo com imagem real e legendas, precisamos de:

## 1. Unsplash API (Imagens Reais) 📸
Gratuito e permite buscar fotos de alta qualidade por palavras-chave.

**Como obter a chave (2 min):**
1. Acesse: https://unsplash.com/oauth/applications
2. Logue ou crie conta.
3. Clique em "New Application".
4. Aceite os termos, dê um nome (ex: "Vector Galaxy").
5. Copie a **Access Key**.

**Cole no `.env`:**
```bash
UNSPLASH_ACCESS_KEY=sua_chave_aqui
```

---

## 2. Legendas (Subtitles) 📝
Vou usar o **Whisper (OpenAI)** rodando localmente (CPU) para transcrever o áudio do ElevenLabs e gerar o arquivo `.srt` com o tempo exato de cada palavra. 

**Vantagem:** 
- Gratuito
- Sincronia labial perfeita
- Acessibilidade total

---

## 3. Workflow de Seleção (Curadoria)

Vou criar um novo script `curate_visuals.py` que:
1. Analisa o roteiro com Gemini para achar palavras-chave de cada cena.
2. Busca 3 opções no Unsplash para cada cena.
3. Gera um arquivo `CURATORIA.md` para você ver as opções.
4. Você escolhe (ou deixa o auto-select) e ele baixa as imagens.

---

**Podemos começar instalando as dependências do Whisper e Unsplash?**
```bash
pip install openai-whisper requests srt
```
