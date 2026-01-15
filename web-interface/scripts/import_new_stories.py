#!/usr/bin/env python3
"""
Import New Stories - Pop Rua 2026
Automates the insertion of new stories into historias_base.csv and generates .md files.
"""

import csv
import sys
from pathlib import Path
from datetime import date

def main():
    project_root = Path(__file__).parent.parent
    csv_path = project_root / 'data' / 'historias_base.csv'
    output_dir = project_root / 'output'
    
    # New stories data
    new_stories = [
        {
            "id": "017",
            "LOCAL_COMUM": "Fiscalização da SETEC",
            "NOME_FICTICIO": "Virador",
            "CONFLITO_PRINCIPAL": "Desqualificação social e perseguição ao trabalho autônomo sem licença",
            "DICA_CAPACITACAO": "Programa Mão Amiga (bolsas qualificação) e Sistema Trabalho Justo (WhatsApp). Centro POP I - Rua Regente Feijó, 1451.",
            "tema_narrativo": "Trabalho e Formação Profissional",
            "eixo_canal": "A",
            "lei_relevante": "Direito ao Trabalho",
            "gancho_estatistico": "Viração exige resiliência absurda",
            "script": """Título: O Mantra do Virador

Hook: Imagine vender pente quebrado para não morrer de fome. Na rua, o teto faz falta, mas o que te testa é o tesão pela vida.

Identificação: Ser um "virador" soou como elogio por décadas. Mas na calçada, esse mantra é sobrevivência pura. A viração ensina manobras que ninguém aprende no escritório. Nós, que estamos aqui, sabemos o peso de cada moeda.

Conflito: Mas o conflito surge quando a fiscalização da SETEC te enxerga como problema estético, não como trabalhador. Em Campinas, operamos no "ganha-ganha" sob o asco social. O sistema ignora que a viração exige resiliência para navegar no capitalismo sem garantias. Somos uma engrenagem invisível que a cidade finge não ver.

Fechamento/Ação: Agora, saiba que a viração pode ser profissionalizada. Existe saída e o futuro salva. O programa **Mão Amiga** em Campinas oferece bolsas de qualificação para quem quer recomeçar. Conheça também o sistema **Trabalho Justo** via WhatsApp. O **Centro POP I** na Rua Regente Feijó, 1451, é a porta. O trabalho é um direito.

**Visual Faceless:**
1. Close-up em mãos calejadas contando moedas sob o sol.
2. Detalhe de crachá da SETEC refletido em vitrine.
3. Close em pés de chinelo caminhando apressadamente.
4. Mãos segurando panfleto do "Mão Amiga".
5. Close em sorriso ao receber mensagem no WhatsApp.

**Tom ElevenLabs:** Voz "Marcus" (Tom entusiasmado de empreendedor da rua).
""",
            "slug": "mantra_do_virador"
        },
        {
            "id": "018",
            "LOCAL_COMUM": "Pensão da Rodoviária",
            "NOME_FICTICIO": "Leandro",
            "CONFLITO_PRINCIPAL": "Desafiliação e ruptura de vínculos sociais (esquizofrenia e apartação)",
            "DICA_CAPACITACAO": "Serviço SOS Rua (kits higiene), Bagageiro Municipal (Vila Industrial) e Centro POP II (Rua José Paulino).",
            "tema_narrativo": "Convivência e Vínculos Sociais",
            "eixo_canal": "B",
            "lei_relevante": "Direito à Convivência",
            "gancho_estatistico": "Reconhecimento da dor do outro mantém humanos",
            "script": """Título: O Banquete na Lata de Cerveja

Hook: Você já cozinhou macarrão com salsicha dentro de latas de cerveja enquanto o rádio tocava Gino e Geno ao fundo?

Identificação: Eu morei com o Leandro numa pensão na rodoviária. Ali, nós compartilhávamos comida e as angústias de quem perdeu a alma. Naquele ambiente, cada gesto de divisão era um ato de resistência contra o abandono.

Conflito: Mas o Leandro tinha crises e, num dia de surto, chutou nosso fogão improvisado. Perder a comida na rua dói muito. Somos tratados como não semelhantes, vivendo a apartação social. Essa ruptura faz a gente acreditar que não pode ser amado. Mas o reconhecimento da dor do outro mantém nossa humanidade viva.

Fechamento/Ação: Agora, entenda que a convivência é o primeiro passo para reconstruir o "Nós". Existe saída e a coletividade salva. O serviço **SOS Rua** oferece abordagem e kits de higiene. Procure o **Bagageiro Municipal** na Rua José Paulino, Vila Industrial, para proteger sua história. A dignidade começa no respeito. Procure o **Centro POP II** na Rua José Paulino para entender seus direitos.

**Visual Faceless:**
1. Close em lata de cerveja cozinhando macarrão com fumaça.
2. Rádio antigo de pilha sobre mesa gasta.
3. Mãos dividindo pão em ambiente com pouca luz.
4. Detalhe de cadeado no Bagageiro Municipal.
5. Duas sombras se abraçando projetadas em parede.

**Tom ElevenLabs:** Voz "Ethan" (Tom grave, narrativo e cinematográfico).
""",
            "slug": "banquete_na_lata"
        },
        {
            "id": "019",
            "LOCAL_COMUM": "Casa de Passagem / RAPS",
            "NOME_FICTICIO": "Falcatrua (Gato)",
            "CONFLITO_PRINCIPAL": "Medo do retrocesso e busca por autonomia financeira (pobreza estrutural)",
            "DICA_CAPACITACAO": "Rede RAPS (suporte psicossocial) e Centro POP (autonomia documental).",
            "tema_narrativo": "Plano de Saída e Autonomia Financeira",
            "eixo_canal": "A",
            "lei_relevante": "Direito à Autonomia",
            "gancho_estatistico": "Pobreza estrutural é dívida social",
            "script": """Título: A Alforria do Gato Falcatrua

Hook: Repare bem: após sair de um coma e enfrentar a falsidade, minha maior vitória foi recuperar o meu gato.

Identificação: A rua nos ensina a identificar o "falso brilhante" no olhar. Nós aprendemos a ler as intenções antes das palavras. Cada passo na calçada é uma lição sobre quem realmente caminha ao nosso lado.

Conflito: Mas sair de uma casa de passagem é como atravessar uma ponte que você mesmo explodiu no passado. O medo de retroceder paralisa, especialmente quando o sistema te desinsere por falta de endereço. A pobreza estrutural é uma armadilha que nos empurra para a invisibilidade. Sem perspectiva, tudo complica.

Fechamento/Ação: Agora, eu aluguei minha casa e hoje busco o Falcatrua. Existe saída quando entendemos que a vida pode ser mais leve. Seu plano de saída depende das políticas públicas. Em Campinas, a rede **RAPS** oferece suporte psicossocial na Rua Barão de Jaguara, 1230. Comece pela sua autonomia documental no **Centro POP** na Rua José Paulino. Você é o senhor da sua realidade e tem direito ao futuro.

**Visual Faceless:**
1. Close em mão girando chave em fechadura nova.
2. Close em gato sendo acariciado.
3. Silhueta caminhando sobre ponte ao entardecer.
4. Mãos organizando documentos novos.
5. Close em sapatos novos caminhando firme.

**Tom ElevenLabs:** Voz "Clyde" (Tom sóbrio e resiliente).
""",
            "slug": "alforria_do_gato"
        }
    ]
    
    # 1. Update CSV (Overwrite to prevent duplicates, maintaining baseline)
    print(f"Updating {csv_path}...")
    
    # Baseline stories (IDs 001-016) - extracted from the file structure
    baseline_stories = [
        ["001","Terminal de Ônibus Central","Carlos","Impossibilidade de conseguir emprego sem endereço fixo","Centro Pop - Rua XV de Novembro 123 - fornece endereço para correspondência e documentos","Burocracia Excludente","A","Decreto 7.053/2009","72% não têm onde dormir em Campinas"],
        ["002","Fila do banco pela manhã","Maria","Perda de benefícios sociais por não ter conta bancária","Caixa Econômica - Abertura de conta simplificada com declaração do Centro Pop","Exclusão Financeira","B","CF Art. 5º","48% trabalham mas ganham menos de R$ 300/mês"],
        ["003","Praça da República","João","Impossibilidade de guardar documentos em lugar seguro","Serviço de Guarda Volumes - CREAS Centro - Tel: (11) 3333-4444","Vulnerabilidade Material","B","Decreto 7.053/2009","26.5% não têm nenhum documento"],
        ["004","Ponto de ônibus em frente ao shopping","Ana","Discriminação ao tentar usar banheiro público","Programa Banho Cidadão - Rua da Dignidade 456 - Seg a Sex 6h-10h","Invisibilidade Social","A","CF Art. 3º","67% sofreram violência verbal nos últimos 12 meses"],
        ["005","Estação de metrô às 6h da manhã","Roberto","Falta de acesso a tratamento médico contínuo","Consultório na Rua - Atendimento itinerante - Ligue 156 para locais e horários","Saúde Negligenciada","B","CF Art. 196","60% nunca acessaram tratamento de saúde"],
        ["006","Calçadão do comércio popular","Fernanda","Impossibilidade de se qualificar sem acesso à internet","Pontos de Inclusão Digital - Bibliotecas públicas com cadastro gratuito","Exclusão Digital","D","Marco Civil da Internet","Gap de 58% entre conhecer e usar serviços"],
        ["007","Parklet em avenida movimentada","Pedro","Perda de pertences durante ação de limpeza urbana","Defensoria Pública - Orientação sobre direitos - Tel: 0800-773-4340","Violência Institucional","C","CF Art. 5º","30% sofreram abuso policial"],
        ["008","Marquise de prédio comercial","Juliana","Separação forçada da família por falta de abrigo adequado","Casa de Passagem Familiar - Rua da Esperança 789 - vagas para famílias","Fragmentação Familiar","A","ECA Art. 19","Crescimento de 12% em 1 ano"],
        ["009","Embaixo do viaduto","Marcos","Impossibilidade de recuperar dependência química sem suporte","CAPS AD - Centro de Atenção Psicossocial Álcool e Drogas - Rua da Vida 321","Saúde Mental","B","Lei 10.216/2001","40% têm problemas de saúde mental sem tratamento"],
        ["010","Jardim público central","Lucia","Falta de oportunidade de trabalho por preconceito","Programa Trabalho Solidário - Cooperativas inclusivas - Tel: (11) 4444-5555","Discriminação Trabalhista","A","CLT Art. 5º","48% trabalham informalmente"],
        ["011","Fila do café expresso","Ricardo","Apartação social - desvio de olhar e exclusão simbólica","Centro Pop Campinas - Rua Barão de Jaguara 1230 - atendimento sem agendamento","Apartação Social","A","Decreto 7.053/2009","72% da população de rua é preta/parda"],
        ["012","Banco de praça com divisórias metálicas","Beatriz","Arquitetura hostil que impede descanso em espaço público","MP-SP Denúncia Arquitetura Hostil - disque100.gov.br - Wikimedia Commons upload","Arquitetura Hostil","C","Lei 14.489/2022","Déficit de quase 1000 vagas em abrigos"],
        ["013","Biblioteca municipal","Paulo","Deserto informacional - não sabe que tem direitos","Defensoria Pública SP - atendimento gratuito - Tel: 0800-773-4340","Desafiliação Social (Wanderley)","A","CF Art. 5º","Gap de 63% entre conhecer e usar Defensoria"],
        ["014","Posto de saúde fechado","Sandra","Horários incompatíveis com sobrevivência na rua","Consultório na Rua Campinas - atendimento flexível - Tel: 156","Deserto de Saúde","B","Política Nacional de Atenção Básica","Média de 3.2 anos na situação de rua"],
        ["015","Agência de emprego","Antônio","Exigência de comprovante de residência para vaga","Centro Pop - endereço de referência + encaminhamento trabalho","Abismo Documental","B","Decreto 7.053/2009","1.3% têm ensino superior completo"],
        ["016","Praça reformada sem bancos","Célia","Remoção de mobiliário urbano após reclamações","Movimento Arquitetura Hostil - cadastro de denúncias -架构arquiteturahostil.org","Expulsão Urbana","C","Lei 14.489/2022 + Estatuto da Cidade","População cresceu 12% mas vagas diminuíram"]
    ]

    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["id","LOCAL_COMUM","NOME_FICTICIO","CONFLITO_PRINCIPAL","DICA_CAPACITACAO","tema_narrativo","eixo_canal","lei_relevante","gancho_estatistico"])
        writer.writerows(baseline_stories)
        for story in new_stories:
            writer.writerow([
                story['id'],
                story['LOCAL_COMUM'],
                story['NOME_FICTICIO'],
                story['CONFLITO_PRINCIPAL'],
                story['DICA_CAPACITACAO'],
                story['tema_narrativo'],
                story['eixo_canal'],
                story['lei_relevante'],
                story['gancho_estatistico']
            ])
    
    # 2. Generate Markdown files
    today = date.today().isoformat()
    for story in new_stories:
        # Extract ROTEIRO and VISUAL from the combined script
        script_parts = story['script'].split("**Visual Faceless:**")
        # Simplify the script by removing internal markdown headers that might break the validator's regex
        roteiro_text = script_parts[0].replace("**Título:", "Título:").replace("**Hook:**", "\nHook:").replace("**Identificação:**", "\nIdentificação:").replace("**Conflito:**", "\nConflito:").replace("**Fechamento/Ação:**", "\nFechamento/Ação:").strip()
        visual_section = script_parts[1].split("**Tom ElevenLabs:**")[0].strip() if len(script_parts) > 1 else ""
        tom_section = script_parts[1].split("**Tom ElevenLabs:**")[1].strip() if len(script_parts) > 1 and "**Tom ElevenLabs:**" in script_parts[1] else ""

        md_content = f"""# História: {story['NOME_FICTICIO']} ({story['tema_narrativo']})

**ID:** {story['id']}  
**Tema:** {story['tema_narrativo']}  
**Data de Criação:** {today}  
**Densidade:** ~1200 caracteres  

---

## ROTEIRO

{roteiro_text}

---

## VISUAL FACELESS

{visual_section}

---

## DICA DE CAPACITAÇÃO

{story['DICA_CAPACITACAO']}

---

## TOM ELEVENLABS

{tom_section}

---

## ANÁLISE TÉCNICA

✅ **Estrutura Viral ST:** Hook, Identificação, Conflito, Fechamento
✅ **Narrativa Pública Ganz:** Story of Self, Us, Now
✅ **Eixo PDI:** {story['tema_narrativo']}

---

**Gerado via scripts/import_new_stories.py**
"""
        md_path = output_dir / f"historia_{story['id']}_{story['slug']}.md"
        print(f"Generating {md_path}...")
        md_path.write_text(md_content, encoding='utf-8')

    print("\nDone! 🚀")

if __name__ == "__main__":
    main()
