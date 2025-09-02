import pandas as pd
import streamlit as st


def safe_dataframe_display(df, key_suffix=""):
    try:
        display_df = df.copy()

        important_cols = []
        for col in [
            "title",
            "source",
            "pub_date",
            "sentiment_class",
            "sentiment_score",
            "description",
        ]:
            if col in display_df.columns:
                important_cols.append(col)

        if important_cols:
            display_df = display_df[important_cols]

        for col in display_df.columns:
            if display_df[col].dtype == "object":
                display_df[col] = display_df[col].astype(str).str[:100]

        for col in display_df.columns:
            if col == "sentiment_score":
                display_df[col] = pd.to_numeric(
                    display_df[col], errors="coerce"
                ).fillna(0.0)
            else:
                display_df[col] = display_df[col].astype(str)

        st.dataframe(display_df, key=f"df_{key_suffix}")

    except Exception as e:
        st.error(f"Erro ao exibir dados: {str(e)}")
        st.write("Estrutura do DataFrame:")
        st.write(f"Shape: {df.shape}")
        st.write(f"Colunas: {list(df.columns)}")
        st.write(f"Tipos: {df.dtypes.to_dict()}")
