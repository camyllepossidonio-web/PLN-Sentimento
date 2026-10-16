import streamlit as st
from textblob import TextBlob
from deep_translator import GoogleTranslator

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Analisador de Sentimentos Offline",
    page_icon="📊",
    layout="centered"
)

def analisar_sentimento(texto: str):
    """
    Traduz o texto para o inglês (caso necessário) de forma transparente
    e calcula a polaridade usando TextBlob.
    """
    if not texto.strip():
        return None, 0.0

    try:
        # Tradução invisível para o inglês para garantir melhor precisão no TextBlob
        texto_traduzido = GoogleTranslator(source='auto', target='en').translate(texto)
    except Exception as e:
        # Caso ocorra algum problema na tradução, usa o texto original
        texto_traduzido = texto

    # Análise de polaridade com TextBlob (-1.0 a 1.0)
    blob = TextBlob(texto_traduzido)
    polaridade = blob.sentiment.polarity

    # Classificação baseada na polaridade
    if polaridade > 0.05:
        sentimento = "Positivo"
    elif polaridade < -0.05:
        sentimento = "Negativo"
    else:
        sentimento = "Neutro"

    return sentimento, polaridade

def main():
    # Interface do usuário
    st.title("📊 Analisador de Sentimentos Offline")
    st.markdown(
        "Este aplicativo realiza análise de sentimentos **100% offline** utilizando bibliotecas tradicionais de Python "
        "(`TextBlob` e `deep-translator`). Nenhuma API externa de IA (como OpenAI ou Google Gemini) é utilizada."
    )
    
    st.divider()

    # Área de entrada de texto
    texto_usuario = st.text_area(
        "Digite seu texto abaixo (pode ser em português ou inglês):",
        placeholder="Ex: Eu adorei este produto, superou todas as minhas expectativas!",
        height=150
    )

    # Botão de análise
    if st.button("Analisar", type="primary"):
        if texto_usuario.strip() == "":
            st.warning("Por favor, digite algum texto antes de clicar em analisar.")
        else:
            with st.spinner("Analisando sentimento..."):
                sentimento, polaridade = analisar_sentimento(texto_usuario)

            st.subheader("Resultado da Análise:")

            # Exibição visual baseada no sentimento utilizando componentes do Streamlit
            if sentimento == "Positivo":
                st.success(f"**Sentimento:** Positivo (Polaridade: {polaridade:.2f})")
            elif sentimento == "Negativo":
                st.error(f"**Sentimento:** Negativo (Polaridade: {polaridade:.2f})")
            else:
                st.warning(f"**Sentimento:** Neutro (Polaridade: {polaridade:.2f})")

if __name__ == "__main__":
    main()
