import re
import time

import requests
import streamlit as st

# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================
st.set_page_config(
    page_title="Studio TikTok Shop IA",
    page_icon="🎬",
    layout="centered"
)

# O Flash-Lite é otimizado para tarefas rápidas e de alto volume.
# Se estiver indisponível, o aplicativo tenta os modelos seguintes.
GEMINI_MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.6-flash",
    "gemini-3.8-flash",
]

GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent"

# =========================================================
# CHAVE DA API
# =========================================================
try:
    API_KEY = st.secrets.get("GEMINI_API_KEY", "")
except Exception:
    API_KEY = ""

if not API_KEY:
    st.error(
        "⚠️ Chave GEMINI_API_KEY não encontrada. "
        "Configure-a em Settings > Secrets no Streamlit."
    )


# =========================================================
# FUNÇÃO PARA CHAMAR A API GEMINI COM MODELO ALTERNATIVO
# =========================================================
def chamar_gemini(prompt_texto):
    if not API_KEY:
        return (
            "**Configuração pendente:** a chave GEMINI_API_KEY não foi "
            "encontrada nos Secrets do Streamlit."
        )

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt_texto}]
            }
        ],
        "generationConfig": {
            "temperature": 0.8,
            "maxOutputTokens": 2048
        }
    }

    erros = []

    for modelo in GEMINI_MODELS:
        url = GEMINI_API_BASE.format(modelo)

        # Duas tentativas no modelo atual antes de passar ao próximo.
        for tentativa in range(2):
            try:
                response = requests.post(
                    url,
                    headers=headers,
                    params={"key": API_KEY},
                    json=payload,
                    timeout=60
                )
            except requests.exceptions.Timeout:
                erros.append(f"{modelo}: tempo limite excedido")
                break
            except requests.exceptions.ConnectionError:
                return (
                    "🌐 **Não foi possível conectar ao Google Gemini.** "
                    "Verifique a conexão do aplicativo e tente novamente."
                )
            except requests.exceptions.RequestException as erro:
                erros.append(f"{modelo}: erro de comunicação ({erro})")
                break

            if response.status_code == 200:
                try:
                    data = response.json()
                    candidates = data.get("candidates", [])

                    if not candidates:
                        motivo = data.get("promptFeedback", {}).get(
                            "blockReason",
                            "A API não retornou uma resposta."
                        )
                        return (
                            "⚠️ Não foi possível gerar o texto. "
                            f"Motivo: {motivo}"
                        )

                    partes = candidates[0].get("content", {}).get("parts", [])
                    texto = "\n".join(
                        parte.get("text", "")
                        for parte in partes
                        if parte.get("text")
                    ).strip()

                    if not texto:
                        return "⚠️ O Gemini respondeu, mas não retornou texto."

                    if modelo != GEMINI_MODELS[0]:
                        return (
                            f"ℹ️ *Modelo alternativo utilizado: {modelo}*\n\n"
                            f"{texto}"
                        )

                    return texto

                except (ValueError, KeyError, IndexError, TypeError):
                    return (
                        "⚠️ Não foi possível interpretar a resposta "
                        "recebida do Gemini."
                    )

            try:
                detalhe = response.json().get("error", {}).get(
                    "message", response.text
                )
            except ValueError:
                detalhe = response.text

            status = response.status_code

            if status in (401, 403):
                return (
                    "🔑 **Problema com a chave ou permissão da API.** "
                    "Confira se a GEMINI_API_KEY está correta e ativa. "
                    f"Detalhe: {detalhe}"
                )

            if status == 400:
                return (
                    "❌ **A API recusou a solicitação (400).** "
                    f"Detalhe: {detalhe}"
                )

            # 404: modelo não disponível para a chave.
            # 429/5xx: limite temporário ou instabilidade; tenta novamente
            # uma vez e depois passa ao próximo modelo.
            if status in (404, 429, 500, 502, 503, 504):
                erros.append(f"{modelo}: HTTP {status} - {detalhe}")
                if tentativa == 0 and status != 404:
                    time.sleep(1.5)
                    continue
                break

            return (
                f"❌ **Erro na API (HTTP {status}).** "
                f"Detalhe: {detalhe}"
            )

    resumo_erros = "\n".join(f"- {erro}" for erro in erros)
    return (
        "❌ **Não foi possível obter resposta de nenhum dos modelos "
        "configurados.**\n\n"
        "O aplicativo tentou os modelos alternativos, mas a API continuou "
        "indisponível ou recusou as solicitações.\n\n"
        f"{resumo_erros}\n\n"
        "Aguarde alguns minutos e tente novamente. Se persistir, confira "
        "o uso e os limites da sua chave no Google AI Studio."
    )




# =========================================================
# GERAR NOME SEGURO PARA O ARQUIVO TXT
# =========================================================
def nome_arquivo_txt(produto):
    nome = re.sub(r"[^A-Za-z0-9_-]+", "_", produto.strip())
    nome = nome.strip("_-") or "roteiro"
    return f"roteiro_{nome[:50]}.txt"

# =========================================================
# LIMPAR CAMPOS DA PRIMEIRA ABA
# =========================================================
def limpar_campos():
    st.session_state["input_produto"] = ""
    st.session_state["input_beneficio"] = ""
    st.session_state["input_publico"] = ""


# =========================================================
# TÍTULO PRINCIPAL
# =========================================================
st.markdown(
    "<h1 style='text-align: center;'>🎬 Studio TikTok Shop IA</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center; color: gray;'>"
    "Central de Inteligência para criação e engenharia reversa "
    "de roteiros para o TikTok Shop."
    "</p>",
    unsafe_allow_html=True
)

# =========================================================
# ABAS
# =========================================================
tab1, tab2 = st.tabs([
    "🎯 Gerar Roteiro do Zero",
    "⚡ Engenharia Reversa (Hooks)"
])

# =========================================================
# ABA 1: GERAR ROTEIRO DO ZERO
# =========================================================
with tab1:
    st.subheader("Criar Roteiro Persuasivo para Vendas")
    st.markdown(
        "Preencha os dados abaixo para gerar um roteiro otimizado "
        "para o TikTok Shop."
    )

    produto = st.text_input(
        "Nome do Produto:",
        placeholder="Ex: Bermuda Jeans Cross",
        key="input_produto"
    )

    beneficio = st.text_input(
        "Principal Benefício / O que ele resolve:",
        placeholder="Ex: Tecido leve para o dia a dia",
        key="input_beneficio"
    )

    publico = st.text_input(
        "Público-Alvo:",
        placeholder="Ex: Pessoas que buscam praticidade no dia a dia",
        key="input_publico"
    )

    tom = st.selectbox(
        "Tom de Voz:",
        [
            "Curiosidade / Impacto",
            "Humor e Descontração",
            "Autoridade / Sinceridade",
            "Urgência / Escassez"
        ]
    )

    col1, col2 = st.columns(2)

    with col1:
        gerar = st.button(
            "🚀 Gerar Roteiro",
            use_container_width=True
        )

    with col2:
        st.button(
            "🗑️ Limpar Campos",
            use_container_width=True,
            on_click=limpar_campos
        )

    if gerar:
        if not produto.strip() or not beneficio.strip():
            st.warning(
                "Por favor, preencha pelo menos o Nome do Produto "
                "e o Principal Benefício."
            )
        else:
            with st.spinner(
                "A inteligência artificial está criando seu roteiro..."
            ):
                system_instruction = (
                    "Você é um especialista em criação de roteiros curtos "
                    "para vídeos de produtos. Gere um roteiro de 30 a 60 "
                    "segundos, com linguagem natural, estruturado em: "
                    "1. Três opções diferentes de gancho inicial; "
                    "2. Apresentação do problema e da solução; "
                    "3. Demonstração ou explicação do produto; "
                    "4. Chamada para ação clara. "
                    "Não invente características, resultados, garantias, "
                    "preços, descontos, estoque limitado ou urgência que "
                    "não tenham sido informados. Identifique qual gancho "
                    "recomenda e use-o no roteiro completo."
                )

                prompt_completo = (
                    f"{system_instruction}\n\n"
                    f"Crie o roteiro com base nestes dados:\n"
                    f"- Produto: {produto}\n"
                    f"- Benefício principal: {beneficio}\n"
                    f"- Público-alvo: {publico or 'Não especificado'}\n"
                    f"- Tom de voz: {tom}\n\n"
                    "Entregue os três ganchos, indique o mais forte e "
                    "apresente o roteiro com falas sugeridas e cenas."
                )

                resultado = chamar_gemini(prompt_completo)

                st.markdown("---")
                st.subheader("💡 Resultado:")
                st.markdown(resultado)

                if not resultado.startswith(("❌", "⚠️", "🔑", "🌐")):
                    st.download_button(
                        label="📄 Baixar roteiro em TXT",
                        data=resultado,
                        file_name=nome_arquivo_txt(produto),
                        mime="text/plain",
                        use_container_width=True,
                        key="download_txt_zero"
                    )


# =========================================================
# ABA 2: ENGENHARIA REVERSA DE HOOKS
# =========================================================
with tab2:
    st.subheader("Engenharia Reversa de Vídeos em Alta")
    st.markdown(
        "Cole a transcrição ou a ideia de um vídeo para analisar sua "
        "estrutura e criar uma versão inédita adaptada ao seu produto."
    )

    video_viral_texto = st.text_area(
        "Transcrição ou Ideia do Vídeo de Referência:",
        placeholder="Cole aqui o que é dito no vídeo que deseja analisar..."
    )

    produto_usuario_rv = st.text_input(
        "Seu produto para adaptar:",
        placeholder="Ex: Bermuda Jeans"
    )

    remodelar = st.button(
        "🔄 Remodelar Roteiro",
        use_container_width=True
    )

    if remodelar:
        if not video_viral_texto.strip() or not produto_usuario_rv.strip():
            st.warning(
                "Por favor, preencha a transcrição ou ideia do vídeo "
                "e informe seu produto."
            )
        else:
            with st.spinner(
                "Analisando o gancho e a estrutura do vídeo..."
            ):
                system_instruction_rv = (
                    "Você é um especialista em análise de roteiros e "
                    "copywriting. Analise o gancho, a estrutura narrativa, "
                    "o ritmo e os recursos de persuasão do texto fornecido. "
                    "Em seguida, crie uma versão original para o novo "
                    "produto. Não copie frases marcantes do texto de "
                    "referência e não invente características, resultados, "
                    "garantias, preços, descontos, estoque limitado ou "
                    "urgência que não tenham sido informados."
                )

                prompt_rv_completo = (
                    f"{system_instruction_rv}\n\n"
                    f"Texto de referência:\n{video_viral_texto}\n\n"
                    f"Produto para adaptar:\n{produto_usuario_rv}\n\n"
                    "Entregue: análise breve do gancho e da estrutura, "
                    "três opções de novos ganchos, indique o mais forte "
                    "e crie um roteiro original com cenas e chamada "
                    "para ação."
                )

                resultado_rv = chamar_gemini(prompt_rv_completo)

                st.markdown("---")
                st.subheader("🚀 Novo Roteiro:")
                st.markdown(resultado_rv)

                if not resultado_rv.startswith(("❌", "⚠️", "🔑", "🌐")):
                    st.download_button(
                        label="📄 Baixar roteiro em TXT",
                        data=resultado_rv,
                        file_name=nome_arquivo_txt(produto_usuario_rv),
                        mime="text/plain",
                        use_container_width=True,
                        key="download_txt_reversa"
                    )
