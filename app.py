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


# =========================================================
# IDENTIDADE VISUAL: ESMERALDA PROFUNDO + DOURADO & COBRE
# =========================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --primaria: #0F5132;
        --primaria-hover: #146c43;
        --destaque: #D9A036;
        --fundo: #F4F9F6;
        --texto: #1F2D24;
        --texto-suave: #5C6B62;
    }

    html, body, [class*="css"], button, input, textarea {
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
    }

    html, body, .stApp {
        color-scheme: light !important;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 8% 0%, rgba(217,160,54,.12), transparent 35%),
            radial-gradient(ellipse at 95% 12%, rgba(15,81,50,.08), transparent 35%),
            var(--fundo) !important;
        color: var(--texto) !important;
        font-size: 16px !important;
    }

    [data-testid="stHeader"] {
        background: rgba(244,249,246,.94) !important;
    }

    [data-testid="stAppViewContainer"] > .main {
        background: transparent !important;
    }

    /* Tipografia */
    h1, h2, h3, h4, p, label, .stMarkdown, [data-testid="stWidgetLabel"] {
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
        color: var(--texto);
    }

    h1 {
        color: #0F5132 !important;
        font-size: 2.25rem !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }

    h2 {
        color: #146c43 !important;
        font-size: 1.65rem !important;
        font-weight: 700 !important;
    }

    h3 {
        color: #146c43 !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
    }

    p, .stMarkdown {
        font-size: 1rem !important;
        line-height: 1.65 !important;
    }

    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] label,
    .stTextInput label, .stTextArea label, .stSelectbox label {
        color: #2D4034 !important;
        font-size: 1rem !important;
        font-weight: 650 !important;
    }

    [data-testid="stCaptionContainer"] {
        color: var(--texto-suave) !important;
        font-size: .92rem !important;
    }

    /* Abas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        border-bottom: 2px solid #D8E7DE;
    }

    .stTabs [data-baseweb="tab"] {
        background: #E2EFE7 !important;
        color: #2D5A42 !important;
        border-radius: 12px 12px 0 0;
        padding: 12px 20px;
        border: 1px solid #C5E1D1;
        font-size: .98rem !important;
        font-weight: 600 !important;
    }

    .stTabs [aria-selected="true"] {
        background: #0F5132 !important;
        color: #FFFFFF !important;
        border-bottom: 3px solid #D9A036 !important;
        font-weight: 750 !important;
    }

    /* Campos de Entrada */
    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea,
    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea {
        background: #FFFFFF !important;
        color: #1F2D24 !important;
        -webkit-text-fill-color: #1F2D24 !important;
        caret-color: #0F5132 !important;
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        line-height: 1.5 !important;
        border-radius: 10px !important;
    }

    [data-testid="stTextInput"] [data-baseweb="input"],
    [data-testid="stTextArea"] [data-baseweb="textarea"],
    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div {
        background: #FFFFFF !important;
        border: 1px solid #C5E1D1 !important;
        border-radius: 11px !important;
        box-shadow: 0 2px 8px rgba(15,81,50,.06) !important;
    }

    /* Select */
    [data-testid="stSelectbox"] [data-baseweb="select"] > div,
    div[data-baseweb="select"] > div {
        background: #FFFFFF !important;
        color: #1F2D24 !important;
        border: 1px solid #C5E1D1 !important;
        border-radius: 11px !important;
        min-height: 44px;
        box-shadow: 0 2px 8px rgba(15,81,50,.06) !important;
    }

    [data-testid="stSelectbox"] [data-baseweb="select"] *,
    div[data-baseweb="select"] * {
        color: #1F2D24 !important;
        -webkit-text-fill-color: #1F2D24 !important;
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
        font-size: 1rem !important;
    }

    [data-baseweb="popover"],
    [data-baseweb="menu"],
    [role="listbox"],
    [role="option"] {
        background: #FFFFFF !important;
        color: #1F2D24 !important;
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
        font-size: .98rem !important;
    }

    [role="option"]:hover {
        background: #E2EFE7 !important;
    }

    input::placeholder, textarea::placeholder {
        color: #8A9A90 !important;
        -webkit-text-fill-color: #8A9A90 !important;
        opacity: 1 !important;
    }

    [data-testid="stTextInput"] input:focus,
    [data-testid="stTextArea"] textarea:focus {
        background: #FFFFFF !important;
        color: #1F2D24 !important;
    }

    [data-testid="stTextInput"] [data-baseweb="input"]:focus-within,
    [data-testid="stTextArea"] [data-baseweb="textarea"]:focus-within,
    [data-testid="stSelectbox"] [data-baseweb="select"]:focus-within {
        border-color: #0F5132 !important;
        box-shadow: 0 0 0 2px rgba(15,81,50,.15) !important;
    }

    /* Botões */
    .stButton > button,
    .stDownloadButton > button {
        border-radius: 12px;
        border: 1px solid #0F5132;
        background: linear-gradient(100deg, #0F5132, #198754);
        color: #FFFFFF !important;
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
        font-size: .98rem !important;
        font-weight: 700 !important;
        min-height: 46px;
        box-shadow: 0 4px 12px rgba(15,81,50,.18);
        transition: transform .15s ease, box-shadow .15s ease;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        border-color: #146c43;
        background: linear-gradient(100deg, #146c43, #218838);
        color: #FFFFFF !important;
        box-shadow: 0 6px 16px rgba(15,81,50,.25);
        transform: translateY(-1px);
    }

    .stButton > button:focus,
    .stDownloadButton > button:focus {
        box-shadow: 0 0 0 3px rgba(217,160,54,.35) !important;
    }

    /* Cartões e Alertas */
    [data-testid="stAlert"] {
        border-radius: 12px;
        border: 1px solid #D8E7DE;
        background: #FFFFFF !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #D8E7DE;
        border-radius: 14px;
        background: rgba(255,255,255,.75);
    }

    hr {
        border-color: #D8E7DE;
    }

    .block-container {
        padding-top: 2.2rem;
        padding-bottom: 3rem;
        max-width: 900px;
    }

    @media (max-width: 640px) {
        .block-container {
            padding-top: 1.2rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        h1 { font-size: 1.8rem !important; }

        .stTabs [data-baseweb="tab"] {
            padding: 10px 12px;
            font-size: .9rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)


# O Flash-Lite é otimizado para tarefas rápidas e de alto volume.
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
                    f"Entregue os três ganchos, indique o mais forte e "
                    f"apresente o roteiro com falas sugeridas e cenas."
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
                    f"Entregue: análise breve do gancho e da estrutura, "
                    f"três opções de novos ganchos, indique o mais forte "
                    f"e crie um roteiro original com cenas e chamada "
                    f"para ação."
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
