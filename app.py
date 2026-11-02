import streamlit as st
import google.generativeai as genai

# Configuração da Página
st.set_page_config(
    page_title="Studio TikTok Shop IA",
    page_icon="🎬",
    layout="centered"
)

# Configuração da Chave de API do Gemini via Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("⚠️ Chave GEMINI_API_KEY não encontrada nos Secrets do Streamlit.")

# Título Principal
st.markdown("<h1 style='text-align: center;'>🎬 Studio TikTok Shop IA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Central de Inteligência para criação e engenharia reversa de roteiros virais para o TikTok Shop.</p>", unsafe_allow_html=True)

# Criação das Abas
tab1, tab2 = st.tabs(["🎯 Gerar Roteiro do Zero", "⚡ Engenharia Reversa (Hooks)"])

# ==========================================
# ABA 1: GERAR ROTEIRO DO ZERO
# ==========================================
with tab1:
    st.subheader("Criar Roteiro Persuasivo para Vendas")
    st.markdown("Preencha os dados abaixo para gerar um roteiro otimizado para conversão no TikTok Shop.")

    if "produto" not in st.session_state:
        st.session_state.produto = ""
    if "beneficio" not in st.session_state:
        st.session_state.beneficio = ""
    if "publico" not in st.session_state:
        st.session_state.publico = ""

    produto = st.text_input("Nome do Produto:", value=st.session_state.produto, placeholder="Ex: Bermuda Jeans Cross", key="input_produto")
    beneficio = st.text_input("Principal Benefício / O que ele resolve:", value=st.session_state.beneficio, placeholder="Ex: Não aperta na cintura e modela o corpo", key="input_beneficio")
    publico = st.text_input("Público-Alvo:", value=st.session_state.publico, placeholder="Ex: Mulheres que buscam conforto no dia a dia", key="input_publico")
    
    tom = st.selectbox("Tom de Voz:", [
        "Curiosidade / Impacto",
        "Humor e Descontração",
        "Autoridade / Sinceridade",
        "Urgência / Escassez"
    ])

    col1, col2 = st.columns(2)
    with col1:
        gerar = st.button("🚀 Gerar Roteiro", use_container_width=True)
    with col2:
        limpar = st.button("🗑️ Limpar Campos", use_container_width=True)

    if limpar:
        st.session_state.produto = ""
        st.session_state.beneficio = ""
        st.session_state.publico = ""
        st.rerun()

    if gerar:
        if not produto or not beneficio:
            st.warning("Por favor, preencha pelo menos o Nome do Produto e o Principal Benefício.")
        else:
            with st.spinner("A inteligência artificial está a criar o seu roteiro viral..."):
                try:
                    system_instruction = (
                        "Você é um especialista em marketing digital, copywriting para TikTok Shop e criador de roteiros virais. "
                        "Gere um roteiro de vídeo curto (entre 30 a 60 segundos) altamente persuasivo, estruturado com: "
                        "1. Gancho Inicial (Hook forte nos primeiros 3 segundos para reter atenção). "
                        "2. Apresentação do Problema e Solução (foco no benefício informado). "
                        "3. Chamada para Ação (CTA) clara para clicar no carrinho laranja do TikTok Shop."
                    )
                    
                    prompt = (
                        f"Produto: {produto}\n"
                        f"Benefício Principal: {beneficio}\n"
                        f"Público-Alvo: {publico}\n"
                        f"Tom de Voz: {tom}"
                    )

                    # Utilizando o modelo padrão estável com system_instruction integrado no prompt para evitar erros de versão de API
                    model = genai.GenerativeModel('gemini-1.5-pro')
                    
                    full_prompt = f"{system_instruction}\n\n{prompt}"
                    response = model.generate_content(full_prompt)

                    st.markdown("---")
                    st.subheader("💡 Roteiro Gerado com Sucesso:")
                    st.markdown(response.text)

                except Exception as e:
                    st.error(f"Ocorreu um erro ao comunicar com a API: {e}")

# ==========================================
# ABA 2: ENGENHARIA REVERSA DE HOOKS
# ==========================================
with tab2:
    st.subheader("Engenharia Reversa de Vídeos em Alta")
    st.markdown("Cole a transcrição ou a ideia de um vídeo campeão de vendas para criar uma versão inédita adaptada ao seu produto.")

    video_viral_texto = st.text_area("Transcrição ou Ideia do Vídeo Viral / Concorrente:", placeholder="Cole aqui o que é dito no vídeo que está a vender muito...")
    produto_usuario_rv = st.text_input("O seu produto para adaptar:", placeholder="Ex: Bermuda Jeans")

    if st.button("🔄 Remodelar Roteiro Campeão", use_container_width=True):
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
                        f"Meu produto para adaptar esta estrutura:\n{produto_usuario_rv}"
                    )

                    model = genai.GenerativeModel('gemini-1.5-pro')
                    
                    full_prompt_rv = f"{system_instruction_rv}\n\n{prompt_rv}"
                    response_rv = model.generate_content(full_prompt_rv)

                    st.markdown("---")
                    st.subheader("🚀 Novo Roteiro Remodelado:")
                    st.markdown(response_rv.text)

                except Exception as e:
                    st.error(f"Ocorreu um erro ao gerar a remodelação: {e}")
