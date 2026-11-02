import streamlit as st
import google.generativeai as genai

# Configuração da página
st.set_page_config(
    page_title="Studio TikTok Shop IA",
    page_icon="🎬",
    layout="centered"
)

# Título principal do aplicativo
st.title("🎬 Studio TikTok Shop IA")
st.caption("Central de Inteligência para criação e engenharia reversa de roteiros virais para o TikTok Shop.")

# Configuração da chave de API oculta no servidor (Secrets do Streamlit)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("⚠️ Erro de Configuração: A chave 'GEMINI_API_KEY' não foi encontrada nos Secrets do Streamlit Cloud.")
    st.stop()

# Criação das Abas Principais
aba1, aba2 = st.tabs(["📝 Gerar Roteiro do Zero", "⚡ Engenharia Reversa (Hooks)"])

# ==========================================
# ABA 1: GERADOR POR FORMULÁRIO
# ==========================================
with aba1:
    st.subheader("Criar Roteiro Persuasivo para Vendas")
    st.markdown("Preencha os dados abaixo para gerar um roteiro otimizado para conversão no TikTok Shop.")

    # Função para limpar os campos do formulário usando o st.session_state
    def limpar_formulario():
        st.session_state["input_produto"] = ""
        st.session_state["input_beneficio"] = ""
        st.session_state["input_publico"] = ""
        st.session_state["input_tom"] = "Humor e Descontração"

    # Campos do formulário vinculados ao session_state
    produto = st.text_input("Nome do Produto:", key="input_produto", placeholder="Ex: Bermuda Jeans Cross")
    beneficio = st.text_input("Principal Benefício / O que ele resolve:", key="input_beneficio", placeholder="Ex: Não aperta na cintura e modela o corpo")
    publico = st.text_input("Público-Alvo:", key="input_publico", placeholder="Ex: Mulheres que buscam conforto no dia a dia")
    
    tom = st.selectbox(
        "Tom de Voz:",
        ["Humor e Descontração", "Urgência / Escassez", "Autoridade / Educacional", "Curiosidade / Impacto"],
        key="input_tom"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Botões lado a lado
    col_gerar, col_limpar = st.columns(2)

    with col_gerar:
        btn_gerar = st.button("🚀 Gerar Roteiro", use_container_width=True)

    with col_limpar:
        btn_limpar = st.button("🗑️ Limpar Campos", on_click=limpar_formulario, use_container_width=True)

    # Ação ao clicar em Gerar Roteiro
    if btn_gerar:
        if not produto or not beneficio:
            st.warning("Por favor, preencha pelo menos o nome do produto e o principal benefício.")
        else:
            with st.spinner("A criar roteiro e legendas virais..."):
                try:
                    system_instruction = (
                        "Você é um especialista sênior em marketing digital, tráfego pago e vendas no TikTok Shop. "
                        "Gere um roteiro de vídeo curto altamente persuasivo contendo exatamente: "
                        "1) Três opções de ganchos virais de alto impacto para os primeiros 3 segundos; "
                        "2) O corpo do roteiro dinâmico e focado em conversão e dor do cliente; "
                        "3) Instruções visuais de cenas (B-roll); "
                        "4) Uma legenda criativa com chamada para ação (CTA) e hashtags virais."
                    )
                    
                    prompt_usuario = (
                        f"Crie um roteiro para o TikTok Shop com base nestes dados:\n"
                        f"- Produto: {produto}\n"
                        f"- Benefício principal: {beneficio}\n"
                        f"- Público-alvo: {publico}\n"
                        f"- Tom de voz: {tom}"
                    )

                    model = genai.GenerativeModel(
                        model_name='gemini-1.5-pro',
                        system_instruction=system_instruction
                    )
                    
                    response = model.generate_content(prompt_usuario)
                    
                    st.markdown("---")
                    st.subheader("✨ Roteiro Gerado com Sucesso:")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Ocorreu um erro ao comunicar com a API: {e}")

# ==========================================
# ABA 2: ENGENHARIA REVERSA (KALODATA STYLE)
# ==========================================
with aba2:
    st.subheader("Engenharia Reversa de Vídeos em Alta")
    st.markdown("Cole a transcrição ou a ideia de um vídeo campeão de vendas (visto no Kalodata ou FastMoss) para criar uma versão inédita adaptada ao seu produto.")

    video_viral_texto = st.text_area("Transcrição ou Ideia do Vídeo Viral / Concorrente:", placeholder="Cole aqui o que é dito no vídeo que está a vender muito...")
    produto_usuario_rv = st.text_input("O seu produto para adaptar:", placeholder="Ex: Bermuda Jeans")

    if st.button("⚡ Remodelar Roteiro Campeão", use_container_width=True):
        if not video_viral_texto or not produto_usuario_rv:
            st.warning("Por favor, preencha a transcrição do vídeo viral e o seu produto.")
        else:
            with st.spinner("A analisar o gancho e a estrutura de vendas..."):
                try:
                    system_instruction_rv = (
                        "Você é um especialista em engenharia reversa de vídeos virais para o TikTok Shop. "
                        "Analise a estrutura, o gancho e o gatilho mental do vídeo fornecido pelo usuário e reescreva "
                        "um roteiro 100% inédito e otimizado para vender o novo produto informado, mantendo a mesma energia e dinâmica de conversão."
                    )
                    
                    prompt_rv = (
                        f"Vídeo de referência (em alta):\n{video_viral_texto}\n\n"
                        f"Meu produto para adaptar essa estrutura:\n{produto_usuario_rv}"
                    )

                    model = genai.GenerativeModel(
                        model_name='gemini-1.5-pro',
                        system_instruction=system_instruction
                    )
                    
                    response_rv = model_rv.generate_content(prompt_rv)
                    
                    st.markdown("---")
                    st.subheader("🔥 Novo Roteiro Remodelado:")
                    st.markdown(response_rv.text)
                    
                except Exception as e:
                    st.error(f"Ocorreu um erro ao gerar a remodelagem: {e}")
