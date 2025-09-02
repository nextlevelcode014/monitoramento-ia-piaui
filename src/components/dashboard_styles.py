import streamlit as st


def apply_custom_css():
    st.markdown(
        """
    <style>
        /* Tema principal */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Header personalizado */
        .main-header {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Cards de métricas */
        div[data-testid="metric-container"] {
            background-color: #ffffff;
            border: 1px solid #e1e5e9;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Sidebar personalizada */
        .css-1d391kg {
            background-color: #f8f9fa;
        }
        
        /* Botões de download */
        .stDownloadButton > button {
            background-color: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
        }
        
        /* Tabelas */
        .dataframe {
            border-radius: 5px;
            overflow: hidden;
        }
        
        /* Alertas customizados */
        .custom-alert-success {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        .custom-alert-warning {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        /* Seções */
        .section-divider {
            height: 3px;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            border: none;
            margin: 2rem 0;
            border-radius: 2px;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )


def create_metric_card(title, value, delta=None, delta_color="normal"):
    delta_html = ""
    if delta:
        color = (
            "#28a745"
            if delta_color == "normal"
            else "#dc3545"
            if delta_color == "inverse"
            else "#6c757d"
        )
        delta_html = (
            f'<p style="color: {color}; font-size: 0.8rem; margin: 0;">{delta}</p>'
        )

    st.markdown(
        f"""
    <div style="background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;">
        <h3 style="margin: 0; color: #495057;">{title}</h3>
        <h2 style="margin: 0.5rem 0; color: #667eea;">{value}</h2>
        {delta_html}
    </div>
    """,
        unsafe_allow_html=True,
    )


def create_section_header(title, subtitle="", icon=""):
    st.markdown(
        f"""
    <div style="margin: 2rem 0 1rem 0;">
        <h2 style="color: #495057; border-bottom: 3px solid #667eea; padding-bottom: 0.5rem;">
            {icon} {title}
        </h2>
        {f'<p style="color: #6c757d; margin-top: 0.5rem;">{subtitle}</p>' if subtitle else ""}
    </div>
    """,
        unsafe_allow_html=True,
    )
