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
