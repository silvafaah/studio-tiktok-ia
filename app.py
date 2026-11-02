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
        gap: 12px;
        border-bottom: 2px solid #F0D4CB;
    }

    .stTabs [data-baseweb="tab"] {
        background: #FCE6DF !important;
        color: #A3482D !important;
        border-radius: 12px 12px 0 0;
        padding: 12px 20px;
        border: 1px solid #E6BDB2;
        font-size: 1.08rem !important;
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

    /* FORÇAR SELECTBOX (Tom de Voz) COM FUNDO BRANCO E TEXTO ESCURO (OVERRIDE TOTAL) */
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
            padding: 10px 12px;
            font-size: 1rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)
