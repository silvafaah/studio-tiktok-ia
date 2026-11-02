import streamlit as st
import requests

# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================
st.set_page_config(
    page_title="Studio TikTok Shop IA",
    page_icon="🎬",
    layout="centered"
)

# Modelo atual recomendado na documentação do Gemini para novos projetos.
# Se sua chave não tiver acesso a esse modelo, consulte os modelos disponíveis
# para ela na documentação oficial do Google.
GEMINI_MODEL = "gemini-3.8-flash"
GEMINI_API_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/"
    f"models/{GEMINI_MODEL}:generateContent"
)

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
# FUNÇÃO PARA CHAMAR A API GEMINI
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

    try:
        response = requests.post(
            GEMINI_API_URL,
            headers=headers,
            params={"key": API_KEY},
            json=payload,
            timeout=60
        )

    except requests.exceptions.Timeout:
        return (
            "⏱️ **A solicitação demorou demais.** "
            "Tente novamente em alguns instantes."
        )
    except requests.exceptions.ConnectionError:
        return (
            "🌐 **Não foi possível conectar ao Google Gemini.** "
            "Verifique sua conexão e tente novamente."
        )
    except requests.exceptions.RequestException as erro:
        return f"Erro de comunicação com a API: {erro}"

    if response.status_code != 200:
        try:
            detalhe = response.json().get("error", {}).get(
                "message", response.text
            )
        except ValueError:
            detalhe = response.text

        if response.status_code == 400:
            return (
                "❌ **A API recusou a solicitação (400).** "
                f"Detalhe: {detalhe}"
            )
        elif response.status_code in (401, 403):
            return (
