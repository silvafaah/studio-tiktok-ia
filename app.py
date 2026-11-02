import streamlit as st
from google import genai

# Configuração da página
st.set_page_config(
    page_title="Studio TikTok Shop IA - Chat",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Studio TikTok Shop IA (Chat)")
st.caption("Converse com a IA para criar roteiros virais e legendas instantâneas para o TikTok Shop.")

# Barra lateral para inserir a Chave da API
with st.sidebar:
    st.header("⚙️ Configurações")
    api_key = st.text_input("Gemini API Key:", type="password", help="Insira a sua chave do Google AI Studio.")
    st.markdown("---")
    st.markdown("💡 **Dica:** Adicione este app à tela inicial do seu telemóvel para um acesso rápido!")

# Inicializa o histórico de mensagens no estado da sessão do Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe as mensagens anteriores do chat na tela
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de texto do chat (na parte inferior da tela)
if prompt_usuario := st.chat_input("Digite o nome do produto e o que ele resolve..."):
    
    if not api_key:
        st.error("Por favor, insira a sua Gemini API Key na barra lateral antes de continuar.")
    else:
        # Adiciona a mensagem do usuário ao histórico
        st.session_state.messages.append({"role": "user", "content": prompt_usuario})
        with st.chat_message("user"):
            st.markdown(prompt_usuario)

        # Gera a resposta da IA
        with st.chat_message("assistant"):
            with st.spinner("A criar roteiro e legendas virais..."):
                try:
                    # Configura o cliente do Gemini com a chave fornecida
                    client = genai.Client(api_key=api_key)
                    
                    # Instrução de sistema embutida para guiar a IA como especialista em marketing
                    system_prompt = (
                        "Você é um especialista em marketing digital e vendas no TikTok Shop. "
                        "Sempre que o usuário enviar um produto ou ideia, crie um roteiro de vídeo curto "
                        "altamente persuasivo contendo: 1) Três opções de ganchos virais para os primeiros 3 segundos; "
                        "2) O desenvolvimento rápido e dinâmico focado em conversão; "
                        "3) Uma legenda criativa com chamada para ação (CTA) e hashtags virais."
                    )
                    
                    # Monta o contexto combinando as regras com a mensagem atual do usuário
                    conteudo_completo = f"{system_prompt}\n\nSolicitação do usuário: {prompt_usuario}"
                    
                    response = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=conteudo_completo,
                    )
                    
                    resposta_ia = response.text
                    st.markdown(resposta_ia)
                    
                    # Adiciona a resposta da IA ao histórico
                    st.session_state.messages.append({"role": "assistant", "content": resposta_ia})
                    
                except Exception as e:
                    erro_msg = f"Ocorreu um erro ao comunicar com a API do Gemini: {e}"
                    st.error(erro_msg)
