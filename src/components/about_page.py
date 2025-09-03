import streamlit as st


def about_page():
    st.title("Sobre o Projeto")

    with open("ABOUT.md", "r", encoding="utf-8") as f:
        conteudo_sobre = f.read()

    st.markdown(conteudo_sobre)
