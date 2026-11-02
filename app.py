import os
import streamlit as st
from google import genai

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Studio TikTok Shop IA",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Studio TikTok Shop IA")
st.subheader("Gerador de Roteiros e Legendas Virais")

# Barra lateral para configuração da API Key
with st.sidebar:
    st.header("⚙️ Configurações")
    
    api_key_env = ""
    try:
        api_key_env = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        pass

    api_key = st.text_input("Gemini API Key:", value=api_key_env, type="password")
    st.info("Insira sua chave do Google AI Studio para ativar a IA.")

# Formulário principal
st.markdown("---")
produto = st.text_input("📦 Nome do Produto / Item", placeholder="Ex: Mini Processador Elétrico de Alimentos")
nicho = st.selectbox("📌 Categoria / Nicho", ["Beleza & Maquiagem", "Cozinha & Casa", "Moda & Acessórios", "Tecnologia & Gadgets", "Fitness & Saúde"])
dor_ou_desejo = st.text_area("💡 Qual o principal benefício ou problema que ele resolve?", placeholder="Ex: Tritura alho e cebola em 5 segundos sem deixar cheiro nas mãos e sem sujeira.")

# Botão de geração
if st.button("🚀 Gerar Roteiro & Legenda", use_container_width=True):
    if not api_key:
        st.error("Por favor, insira a Gemini API Key!")
    elif not produto:
        st.warning("Preencha o nome do produto!")
    else:
        with st.spinner("O Gemini está criando um roteiro de alta conversão..."):
            try:
                # Inicializa o cliente oficial da biblioteca google-genai
                client = genai.Client(api_key=api_key)

                prompt = f"""
                Você é um estrategista de conteúdo expert em TikTok Shop no Brasil, especializado em criar vídeos virais de alta retenção e vendas por impulso.

                Crie um roteiro completo de vídeo curto (45 a 60 segundos) para o produto abaixo:
                - Produto: {produto}
                - Categoria: {nicho}
                - Benefício / Dor do cliente: {dor_ou_desejo}

                Siga ESTRITAMENTE este formato de resposta em Markdown legível:

                ### 🎯 OPÇÕES DE GANCHOS (Primeiros 3 segundos - Escolha 1)
                - Opção 1 (Visual/Choque): [Texto]
                - Opção 2 (Pergunta/Curiosidade): [Texto]
                - Opção 3 (Dor Direta): [Texto]

                ---
                ### 📜 ROTEIRO PASSO A PASSO (45-60s)
                * **[00:00 - 00:05] Gancho:** (Fala e indicação de cena)
                * **[00:05 - 00:15] O Problema:** (Mostrar a dor de forma natural)
                * **[00:15 - 00:35] A Solução / Demonstração:** (Mostrar o produto em ação e o benefício)
                * **[00:35 - 00:45] Chamada para Ação (CTA):** (Apontando para o carrinho laranja do TikTok Shop)

                ---
                ### 📝 LEGENDA PRONTA PARA O TIKTOK
                [Escreva uma legenda persuasiva e curta com emojis + 5 hashtags estratégicas em alta para esse nicho no Brasil]
                """

                # Chamada para o modelo rápido e eficiente do Gemini
                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=prompt
                )

                st.success("Roteiro gerado com sucesso!")
                st.markdown("---")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Erro ao conectar com a API do Gemini: {e}")