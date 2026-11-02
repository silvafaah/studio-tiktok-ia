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
# IDENTIDADE VISUAL: LAVANDA + ROSA-PÊSSEGO
# =========================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --lavanda: #8B72C8;
        --lavanda-escuro: #7056AD;
        --rosa: #F3A6B8;
        --fundo: #FFF9FC;
        --texto: #40364D;
        --texto-suave: #746A7D;
    }

    html, body, [class*="css"], button, input, textarea {
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
    }

    html, body, .stApp {
        color-scheme: light !important;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 8% 0%, rgba(243,166,184,.18), transparent 34%),
            radial-gradient(ellipse at 95% 12%, rgba(168,216,197,.20), transparent 32%),
            var(--fundo) !important;
        color: var(--texto) !important;
        font-size: 16px !important;
    }

    [data-testid="stHeader"] {
        background: rgba(255,249,252,.94) !important;
    }

    [data-testid="stAppViewContainer"] > .main {
        background: transparent !important;
    }

    /* Tipografia: maior, moderna e confortável */
    h1, h2, h3, h4, p, label, .stMarkdown, [data-testid="stWidgetLabel"] {
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
        color: var(--texto);
    }

    h1 {
        color: #7056AD !important;
        font-size: 2.25rem !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }

    h2 {
        color: #795FAF !important;
        font-size: 1.65rem !important;
        font-weight: 700 !important;
    }

    h3 {
        color: #795FAF !important;
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
        color: #51445F !important;
        font-size: 1rem !important;
        font-weight: 650 !important;
    }

    [data-testid="stCaptionContainer"] {
        color: var(--texto-suave) !important;
        font-size: .92rem !important;
    }

    /* Abas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        border-bottom: 2px solid #E9DFF4;
    }

    .stTabs [data-baseweb="tab"] {
        background: #F3ECFA !important;
        color: #695783 !important;
        border-radius: 12px 12px 0 0;
        padding: 12px 19px;
        border: 1px solid #E6D9F2;
        font-size: .98rem !important;
        font-weight: 600 !important;
    }

    .stTabs [aria-selected="true"] {
        background: #E9DDF8 !important;
        color: #62499B !important;
        border-bottom: 3px solid #8B72C8 !important;
        font-weight: 750 !important;
    }

    /* Campos: força fundo branco e texto escuro em todos os elementos internos */
    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea,
    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea {
        background: #FFFFFF !important;
        color: #40364D !important;
        -webkit-text-fill-color: #40364D !important;
        caret-color: #7056AD !important;
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
        border: 1px solid #E5D9EF !important;
        border-radius: 11px !important;
        box-shadow: 0 2px 8px rgba(112,86,173,.06) !important;
    }

    /* Select: texto, fundo, menu e opções */
    [data-testid="stSelectbox"] [data-baseweb="select"] > div,
    div[data-baseweb="select"] > div {
        background: #FFFFFF !important;
        color: #40364D !important;
        border: 1px solid #E5D9EF !important;
        border-radius: 11px !important;
        min-height: 44px;
        box-shadow: 0 2px 8px rgba(112,86,173,.06) !important;
    }

    [data-testid="stSelectbox"] [data-baseweb="select"] *,
    div[data-baseweb="select"] * {
        color: #40364D !important;
        -webkit-text-fill-color: #40364D !important;
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
        font-size: 1rem !important;
    }

    [data-baseweb="popover"],
    [data-baseweb="menu"],
    [role="listbox"],
    [role="option"] {
        background: #FFFFFF !important;
        color: #40364D !important;
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
        font-size: .98rem !important;
    }

    [role="option"]:hover {
        background: #F3ECFA !important;
    }

    input::placeholder, textarea::placeholder {
        color: #9A8FA4 !important;
        -webkit-text-fill-color: #9A8FA4 !important;
        opacity: 1 !important;
    }

    [data-testid="stTextInput"] input:focus,
    [data-testid="stTextArea"] textarea:focus {
        background: #FFFFFF !important;
        color: #40364D !important;
    }

    [data-testid="stTextInput"] [data-baseweb="input"]:focus-within,
    [data-testid="stTextArea"] [data-baseweb="textarea"]:focus-within,
    [data-testid="stSelectbox"] [data-baseweb="select"]:focus-within {
        border-color: #A58BD8 !important;
        box-shadow: 0 0 0 2px rgba(139,114,200,.15) !important;
    }

    /* Botões */
    .stButton > button,
    .stDownloadButton > button {
        border-radius: 12px;
        border: 1px solid #8B72C8;
        background: linear-gradient(100deg, #8B72C8, #A68BD8);
        color: #FFFFFF !important;
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
        font-size: .98rem !important;
        font-weight: 700 !important;
        min-height: 46px;
        box-shadow: 0 4px 10px rgba(112,86,173,.14);
        transition: transform .15s ease, box-shadow .15s ease;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        border-color: #7056AD;
        background: linear-gradient(100deg, #7056AD, #9276C9);
        color: #FFFFFF !important;
        box-shadow: 0 6px 14px rgba(112,86,173,.20);
        transform: translateY(-1px);
    }

    .stButton > button:focus,
    .stDownloadButton > button:focus {
        box-shadow: 0 0 0 3px rgba(243,166,184,.35) !important;
    }

    /* Cartões e mensagens */
    [data-testid="stAlert"] {
        border-radius: 12px;
        border: 1px solid #E9DDF4;
        background: #FFFFFF !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #E9DFF4;
        border-radius: 14px;
        background: rgba(255,255,255,.62);
    }

    hr {
        border-color: #E9DFF4;
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
            padding: 10px 11px;
            font-size: .9rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)


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
