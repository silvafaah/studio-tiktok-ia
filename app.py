
import streamlit as st
import requests

# =========================================================
# CONFIGURACAO DA PAGINA
# =========================================================
st.set_page_config(
    page_title="Studio TikTok Shop IA",
    page_icon="🎬",
    layout="centered"
)

GEMINI_MODEL = "gemini-3.8-flash"

GEMINI_API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/"
    f"models/{GEMINI_MODEL}:generateContent"
)

# =========================================================
# CHAVE DA API
# =========================================================
try:
    API_KEY = st.secrets.get("GEMINI_API_KEY", "")
except Exception:
    API_KEY = ""

# =========================================================
# FUNCAO PARA CHAMAR A API GEMINI
# =========================================================
def chamar_gemini(prompt_texto):

    if not API_KEY:
        return (
            "⚠️ Chave da API não encontrada. "
            "Configure GEMINI_API_KEY em Settings > Secrets "
            "no Streamlit."
        )

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt_texto}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.8,
            "maxOutputTokens": 2048
        }
    }

    try:
        response = requests.post(
            GEMINI_API_URL,
            headers=headers,
            params={"key": API_KEY},
            json=payload,
            timeout=60
        )

    except requests.exceptions.Timeout:
        return "⏱️ Tempo limite excedido. Tente novamente."

    except requests.exceptions.ConnectionError:
        return (
            "🌐 Não foi possível conectar ao Google Gemini. "
            "Verifique sua conexão."
        )

    except requests.exceptions.RequestException as erro:
        return f"Erro de comunicação com a API: {erro}"

    # TRATAMENTO DE ERROS DA API
    if response.status_code != 200:

        try:
            detalhe = response.json().get(
                "error", {}
            ).get("message", response.text)

        except (ValueError, AttributeError):
            detalhe = response.text

        if response.status_code in (401, 403):
            return (
                "🔑 Problema com a chave ou permissão da API. "
                "Confira se GEMINI_API_KEY está correta e ativa. "
                f"Detalhe: {detalhe}"
            )

        elif response.status_code == 404:
            return (
                f"❌ Modelo {GEMINI_MODEL} não encontrado ou "
                "indisponível para esta chave. "
                f"Detalhe: {detalhe}"
            )

        elif response.status_code == 429:
            return (
                "⌛ Limite de solicitações atingido. "
                f"Detalhe: {detalhe}"
            )

        else:
            return (
                f"❌ Erro na API (HTTP {response.status_code}). "
                f"Detalhe: {detalhe}"
            )

    # LEITURA DA RESPOSTA
    try:
        data = response.json()

    except ValueError:
        return "⚠️ A API retornou uma resposta inválida."

    candidates = data.get("candidates", [])

    if not candidates:
        motivo = data.get(
            "promptFeedback", {}
        ).get(
            "blockReason",
            "A API não retornou uma resposta."
        )

        return f"⚠️ Não foi possível gerar o texto. Motivo: {motivo}"

    partes = candidates[0].get(
        "content", {}
    ).get("parts", [])

    texto = "\n".join(
        parte.get("text", "")
        for parte in partes
        if isinstance(parte, dict) and parte.get("text")
    ).strip()

    if not texto:
        return "⚠️ O Gemini respondeu, mas não retornou texto."

    return texto


# =========================================================
# FUNCAO PARA LIMPAR CAMPOS
# =========================================================
def limpar_campos():

    st.session_state["input_produto"] = ""
    st.session_state["input_beneficio"] = ""
    st.session_state["input_publico"] = ""


# =========================================================
# TITULO PRINCIPAL
# =========================================================
st.markdown(
    "<h1 style='text-align: center;'>🎬 Studio TikTok Shop IA</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center; color: gray;'>"
    "Central de Inteligência para criação e engenharia reversa "
    "de roteiros virais para o TikTok Shop."
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
# ABA 1 - GERAR ROTEIRO DO ZERO
# =========================================================
with tab1:

    st.subheader("Criar Roteiro Persuasivo para Vendas")

    st.markdown(
        "Preencha os dados abaixo para gerar um roteiro "
        "otimizado para conversão no TikTok Shop."
    )

    produto = st.text_input(
        "Nome do Produto:",
        placeholder="Ex: Bermuda Jeans Cross",
        key="input_produto"
    )

    beneficio = st.text_input(
        "Principal Benefício / O que ele resolve:",
        placeholder="Ex: Não aperta na cintura e modela o corpo",
        key="input_beneficio"
    )

    publico = st.text_input(
        "Público-Alvo:",
        placeholder="Ex: Pessoas que buscam conforto no dia a dia",
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
                    "Você é um especialista em marketing digital, "
                    "copywriting para TikTok Shop e criação de roteiros "
                    "curtos. Gere um roteiro de vídeo entre 30 e 60 "
                    "segundos, com linguagem natural e persuasiva. "
                    "Estruture em: "
                    "1. Gancho inicial forte nos primeiros 3 segundos; "
                    "2. Apresentação do problema e da solução; "
                    "3. Demonstração ou explicação do produto; "
                    "4. Chamada para ação clara para conhecer o produto "
                    "no TikTok Shop. "
                    "Não invente características, resultados ou garantias "
                    "que não foram informados pelo usuário."
                )

                prompt_completo = (
                    f"{system_instruction}\n\n"
                    "Crie o roteiro com base nestes dados:\n"
                    f"- Produto: {produto}\n"
                    f"- Benefício principal: {beneficio}\n"
                    f"- Público-alvo: {publico or 'Não especificado'}\n"
                    f"- Tom de voz: {tom}\n\n"
                    "Entregue o roteiro com falas sugeridas "
                    "e indicação breve das cenas."
                )

                resultado = chamar_gemini(prompt_completo)

                st.markdown("---")

                st.subheader("💡 Resultado:")

                st.markdown(resultado)


# =========================================================
# ABA 2 - ENGENHARIA REVERSA DE HOOKS
# =========================================================
with tab2:

    st.subheader("Engenharia Reversa de Vídeos em Alta")

    st.markdown(
        "Cole a transcrição ou a ideia de um vídeo para analisar "
        "sua estrutura e criar uma versão inédita adaptada ao seu produto."
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

        if (
            not video_viral_texto.strip()
            or not produto_usuario_rv.strip()
        ):

            st.warning(
                "Por favor, preencha a transcrição ou ideia do vídeo "
                "e informe seu produto."
            )

        else:

            with st.spinner(
                "Analisando o gancho e a estrutura do vídeo..."
            ):

                system_instruction_rv = (
                    "Você é um especialista em análise de roteiros "
                    "e copywriting para TikTok Shop. Analise o gancho, "
                    "a estrutura narrativa, o ritmo e os recursos de "
                    "persuasão do texto fornecido. Em seguida, crie "
                    "um roteiro original para o novo produto. "
                    "Não copie frases marcantes do texto de referência "
                    "e não invente características ou resultados "
                    "do produto."
                )

                prompt_rv_completo = (
                    f"{system_instruction_rv}\n\n"
                    f"Texto de referência:\n{video_viral_texto}\n\n"
                    f"Produto para adaptar:\n{produto_usuario_rv}\n\n"
                    "Entregue: análise breve do gancho, novo gancho, "
                    "roteiro completo com cenas e chamada para ação."
                )

                resultado_rv = chamar_gemini(
                    prompt_rv_completo
                )

                st.markdown("---")

                st.subheader("🚀 Novo Roteiro Remodelado:")

                st.markdown(resultado_rv)
