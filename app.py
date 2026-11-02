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
                    "curtos. Gere um roteiro de vídeo entre 30 e 60 segundos, "
                    "com linguagem natural e persuasiva, estruturado em: "
                    "1. Gancho inicial forte nos primeiros 3 segundos; "
                    "2. Apresentação do problema e da solução, com foco no "
                    "benefício informado; "
                    "3. Demonstração ou explicação do produto; "
                    "4. Chamada para ação clara e adequada para o TikTok Shop. "
                    "Não invente características, resultados ou garantias "
                    "que não foram informados pelo usuário."
                )

                prompt_completo = (
                    f"{system_instruction}\n\n"
                    f"Crie o roteiro com base nestes dados:\n"
                    f"- Produto: {produto}\n"
                    f"- Benefício principal: {beneficio}\n"
                    f"- Público-alvo: {publico or 'Não especificado'}\n"
                    f"- Tom de voz: {tom}\n\n"
                    "Entregue o roteiro com falas sugeridas e indicação "
                    "breve das cenas."
                )

                resultado = chamar_gemini(prompt_completo)

                st.markdown("---")
                st.subheader("💡 Resultado:")
                st.markdown(resultado)


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
                    "copywriting para TikTok Shop. Analise o gancho, a "
                    "estrutura narrativa, o ritmo e os recursos de persuasão "
                    "do texto fornecido. Em seguida, crie um roteiro "
                    "original para o novo produto. Não copie frases "
                    "marcantes do texto de referência e não invente "
                    "características ou resultados do produto."
                )

                prompt_rv_completo = (
                    f"{system_instruction_rv}\n\n"
                    f"Texto de referência:\n{video_viral_texto}\n\n"
                    f"Produto para adaptar:\n{produto_usuario_rv}\n\n"
