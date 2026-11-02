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
# IDENTIDADE VISUAL: PÊSSEGO ACONCHEGANTE + TERRACOTA & COBRE
# =========================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --primaria: #E07A5F;
        --primaria-hover: #CC6B50;
        --destaque: #F4A261;
        --fundo: #FFF8F5;
        --texto: #3D2C2E;
        --texto-suave: #6E585A;
    }

    html, body, [class*="css"], button, input, textarea {
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
    }

    html, body, .stApp {
        color-scheme: light !important;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 8% 0%, rgba(244,162,97,.15), transparent 35%),
            radial-gradient(ellipse at 95% 12%, rgba(224,122,95,.10), transparent 35%),
            var(--fundo) !important;
        color: var(--texto) !important;
        font-size: 18px !important;
    }

    /* Barra superior do Streamlit mais visível e destacada */
    [data-testid="stHeader"] {
        background: #FCECE4 !important;
        border-bottom: 1px solid #F0D4CB !important;
        visibility: visible !important;
    }

    [data-testid="stAppViewContainer"] > .main {
        background: transparent !important;
    }

    /* Tipografia (Aumentada em 2pt) */
    h1, h2, h3, h4, p, label, .stMarkdown, [data-testid="stWidgetLabel"] {
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
        color: var(--texto);
    }

    h1 {
        color: #C85A3B !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }

    h2 {
        color: #D36C4E !important;
        font-size: 1.85rem !important;
        font-weight: 700 !important;
    }

    h3 {
        color: #D36C4E !important;
        font-size: 1.45rem !important;
        font-weight: 700 !important;
    }

    p, .stMarkdown {
        font-size: 1.12rem !important;
        line-height: 1.7 !important;
    }

    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] label,
    .stTextInput label, .stTextArea label, .stSelectbox label {
        color: #4A3538 !important;
        font-size: 1.12rem !important;
        font-weight: 700 !important;
    }

    [data-testid="stCaptionContainer"] {
        color: var(--texto-suave) !important;
        font-size: 1.02rem !important;
    }

    /* Abas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 2px solid #F0D4CB;
    }

    .stTabs [data-baseweb="tab"] {
        background: #FCE6DF !important;
        color: #A3482D !important;
        border-radius: 12px 12px 0 0;
        padding: 10px 16px;
        border: 1px solid #E6BDB2;
        font-size: 0.98rem !important;
        font-weight: 600 !important;
    }

    .stTabs [aria-selected="true"] {
        background: #E07A5F !important;
        color: #FFFFFF !important;
        border-bottom: 3px solid #C85A3B !important;
        font-weight: 750 !important;
    }

    /* Container central para diminuir a largura visual dos inputs */
    .block-container {
        padding-top: 2.2rem;
        padding-bottom: 3rem;
        max-width: 720px;
    }

    /* Campos de Entrada com largura ajustada e fonte maior */
    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea,
    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea {
        background: #FFFFFF !important;
        color: #3D2C2E !important;
        -webkit-text-fill-color: #3D2C2E !important;
        caret-color: #E07A5F !important;
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
        font-size: 1.12rem !important;
        font-weight: 500 !important;
        line-height: 1.5 !important;
        border-radius: 10px !important;
    }

    [data-testid="stTextInput"] [data-baseweb="input"],
    [data-testid="stTextArea"] [data-baseweb="textarea"],
    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div {
        background: #FFFFFF !important;
        border: 1px solid #E6BDB2 !important;
        border-radius: 11px !important;
        box-shadow: 0 2px 8px rgba(224,122,95,.08) !important;
    }

    /* SELECTBOX (Tom de Voz) COM FUNDO BRANCO E TEXTO ESCURO FORÇADO */
    [data-baseweb="select"] {
        background-color: #FFFFFF !important;
    }

    [data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        background-image: none !important;
        color: #3D2C2E !important;
        border-color: #E6BDB2 !important;
        border-radius: 11px !important;
        min-height: 48px;
    }

    [data-baseweb="select"] span, 
    [data-baseweb="select"] div,
    [data-testid="stSelectbox"] div[data-baseweb="select"] span {
        color: #3D2C2E !important;
        -webkit-text-fill-color: #3D2C2E !important;
        font-size: 1.12rem !important;
    }

    /* Menu Popover / Opções do Selectbox */
    [data-baseweb="popover"], [data-baseweb="menu"], [role="listbox"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E6BDB2 !important;
        border-radius: 10px !important;
    }

    [role="option"] {
        background-color: #FFFFFF !important;
        color: #3D2C2E !important;
        font-size: 1.08rem !important;
    }

    [role="option"]:hover {
        background-color: #FCE6DF !important;
        color: #C85A3B !important;
    }

    input::placeholder, textarea::placeholder {
        color: #A8908D !important;
        -webkit-text-fill-color: #A8908D !important;
        opacity: 1 !important;
    }

    [data-testid="stTextInput"] input:focus,
    [data-testid="stTextArea"] textarea:focus {
        background: #FFFFFF !important;
        color: #3D2C2E !important;
    }

    [data-testid="stTextInput"] [data-baseweb="input"]:focus-within,
    [data-testid="stTextArea"] [data-baseweb="textarea"]:focus-within {
        border-color: #E07A5F !important;
        box-shadow: 0 0 0 2px rgba(224,122,95,.20) !important;
    }

    /* Botões */
    .stButton > button,
    .stDownloadButton > button {
        border-radius: 12px;
        border: 1px solid #C85A3B;
        background: linear-gradient(100deg, #E07A5F, #F4A261);
        color: #FFFFFF !important;
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
        font-size: 1.08rem !important;
        font-weight: 700 !important;
        min-height: 50px;
        box-shadow: 0 4px 12px rgba(224,122,95,.22);
        transition: transform .15s ease, box-shadow .15s ease;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        border-color: #A3482D;
        background: linear-gradient(100deg, #CC6B50, #E7934F);
        color: #FFFFFF !important;
        box-shadow: 0 6px 16px rgba(224,122,95,.30);
        transform: translateY(-1px);
    }

    .stButton > button:focus,
    .stDownloadButton > button:focus {
        box-shadow: 0 0 0 3px rgba(244,162,97,.40) !important;
    }

    /* Cartões e Alertas */
    [data-testid="stAlert"] {
        border-radius: 12px;
        border: 1px solid #F0D4CB;
        background: #FFFFFF !important;
        font-size: 1.08rem !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #F0D4CB;
        border-radius: 14px;
        background: rgba(255,255,255,.85);
    }

    hr {
        border-color: #F0D4CB;
    }

    @media (max-width: 640px) {
        .block-container {
            padding-top: 1.2rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        h1 { font-size: 2rem !important; }

        .stTabs [data-baseweb="tab"] {
            padding: 8px 10px;
            font-size: 0.9rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)


GEMINI_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
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
# FUNÇÃO PARA CHAMAR A API GEMINI (TEXTO)
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
        "configurados devido a congestionamento (Alta Demanda).**\n\n"
        "Aguarde alguns segundos e tente novamente.\n\n"
        f"{resumo_erros}"
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
    "Central de Inteligência para criação, transcrição e engenharia reversa "
    "de roteiros para o TikTok Shop."
    "</p>",
    unsafe_allow_html=True
)

# =========================================================
# ABAS DO APLICATIVO
# =========================================================
tab1, tab2, tab3 = st.tabs([
    "🎯 Gerar Roteiro",
    "🎙️ Transcrever Vídeo",
    "⚡ Engenharia Reversa"
])

# =========================================================
# ABA 1: GERAR ROTEIRO DO ZERO
# =========================================================
with tab1:
    st.subheader("Criar Roteiro Persuasivo para Vendas")
    st.markdown(
        "Preencha os dados abaixo para gerar um roteiro otimizado "
        "em tabela estruturada para o TikTok Shop."
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
                    "para vídeos de produtos. Desenvolva um roteiro dinâmico com duração total de 30 a 60 segundos. "
                    "IMPORTANTE: Apresente o roteiro em formato de tabela Markdown contendo DUAS colunas principais: 'Tempo / Bloco' (ex: 00s - 05s) e 'Texto Falado' (a locução/fala direta para a câmera). "
                    "NÃO inclua nenhuma descrição de cenas, diretrizes visuais ou ações. Apenas o tempo na primeira coluna e o texto falado correspondente na segunda coluna."
                )

                prompt_completo = (
                    f"{system_instruction}\n\n"
                    f"Crie o roteiro com base nestes dados:\n"
                    f"- Produto: {produto}\n"
                    f"- Benefício principal: {beneficio}\n"
                    f"- Público-alvo: {publico or 'Não especificado'}\n"
                    f"- Tom de voz: {tom}\n\n"
                    f"Entregue as três opções de gancho inicial, indique a mais forte e, em seguida, monte o roteiro completo estruturado em tabela com o tempo e o texto falado lado a lado, sem cenas."
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
# ABA 2: TRANSCRIÇÃO AUTOMÁTICA DE VÍDEO (COM RESILIÊNCIA A 503)
# =========================================================
with tab2:
    st.subheader("Transcrição de Vídeo por IA")
    st.markdown(
        "Envie o arquivo de vídeo baixado (ex: do TikTok) para extrair "
        "automaticamente a transcrição completa e utilizá-la na engenharia reversa."
    )

    video_arquivo = st.file_uploader(
        "Selecione o arquivo de vídeo (.mp4, .mov, .webm):",
        type=["mp4", "mov", "avi", "mkv", "webm"]
    )

    if video_arquivo is not None:
        st.video(video_arquivo)
        
        if st.button("🎙️ Extrair Transcrição do Vídeo", use_container_width=True):
            with st.spinner("Enviando arquivo e extraindo a transcrição com IA..."):
                try:
                    from google import genai
                    
                    client = genai.Client(api_key=API_KEY)
                    
                    temp_path = "temp_uploaded_video.mp4"
                    with open(temp_path, "wb") as f:
                        f.write(video_arquivo.getbuffer())
                    
                    video_ref = client.files.upload(file=temp_path)
                    
                    while video_ref.state.name == "PROCESSING":
                        time.sleep(2)
                        video_ref = client.files.get(name=video_ref.name)
                    
                    # Tenta os modelos em loop caso o primeiro esteja com alta demanda (503)
                    response_transcricao = None
                    ultimo_erro = None
                    
                    for modelo_transcr in GEMINI_MODELS:
                        try:
                            response_transcricao = client.models.generate_content(
                                model=modelo_transcr,
                                contents=[
                                    video_ref,
                                    "Faça a transcrição palavra por palavra, exata e completa de tudo o que é falado neste vídeo."
                                ]
                            )
                            if response_transcricao and response_transcricao.text:
                                break
                        except Exception as e:
                            ultimo_erro = e
                            time.sleep(1)
                            continue
                    
                    if not response_transcricao or not response_transcricao.text:
                        raise Exception(
                            f"Todos os modelos retornaram erro de alta demanda. Detalhe: {ultimo_erro}"
                        )
                    
                    texto_transcrito = response_transcricao.text
                    
                    st.success("Transcrição concluída com sucesso!")
                    st.text_area(
                        "Texto Transcrito (copie para usar na Engenharia Reversa):",
                        value=texto_transcrito,
                        height=250
                    )
                    
                    st.download_button(
                        label="📄 Baixar transcrição em TXT",
                        data=texto_transcrito,
                        file_name="transcricao_video.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

                except Exception as e:
                    st.error(f"Erro ao processar o vídeo: {e}")


# =========================================================
# ABA 3: ENGENHARIA REVERSA DE HOOKS
# =========================================================
with tab3:
    st.subheader("Engenharia Reversa de Vídeos em Alta")
    st.markdown(
        "Cole a transcrição (ou o texto extraído na aba anterior) para analisar "
        "a estrutura e criar uma versão inédita adaptada ao seu produto."
    )

    video_viral_texto = st.text_area(
        "Transcrição ou Ideia do Vídeo de Referência:",
        placeholder="Cole aqui o que foi dito no vídeo que deseja analisar..."
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
                "Por favor, preencha a transcrição do vídeo "
                "e informe o seu produto."
            )
        else:
            with st.spinner(
                "Analisando o gancho e estruturando o novo roteiro..."
            ):
                system_instruction_rv = (
                    "Você é um especialista em análise de roteiros e "
                    "copywriting. Analise o gancho, a estrutura narrativa, "
                    "o ritmo e os recursos de persuasão do texto fornecido. "
                    "Crie uma versão original em tabela adaptada para o novo produto mantendo o timing ideal de 30 a 60 segundos. "
                    "IMPORTANTE: Apresente o roteiro final em formato de tabela Markdown com as colunas 'Tempo / Bloco' e 'Texto Falado', contendo apenas a locução/fala sem nenhuma descrição de cenas."
                )

                prompt_rv_completo = (
                    f"{system_instruction_rv}\n\n"
                    f"Texto de referência:\n{video_viral_texto}\n\n"
                    f"Produto para adaptar:\n{produto_usuario_rv}\n\n"
                    f"Entregue: análise breve do gancho, três opções de novos ganchos, indique o mais forte e apresente o roteiro original formatado em tabela com tempo e texto falado, sem cenas."
                )

                resultado_rv = chamar_gemini(prompt_rv_completo)

                st.markdown("---")
                st.subheader("🚀 Novo Roteiro em Tabela:")
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
