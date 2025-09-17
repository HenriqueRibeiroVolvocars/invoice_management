import streamlit as st
import os
from PIL import Image
from dotenv import load_dotenv
from app.data import load_suppliers, load_pos, load_notes
from app.ui_sidebar import render_sidebar
from app.ui_notes_form import render_notes_form
from app.ui_notes_table import render_notes_table
from app.ui_analytics import render_analytics, render_supplier_month_pivot
from app.ui_records import render_records_manager
from app.services import copy_invoice_message, copy_po


load_dotenv()

# 1. Carregar a imagem que você quer usar como favicon
try:
    img = Image.open("./assets/Iron Mark/Light Version AI EPS Volvo Iron Mark  white.png") # Substitua "seu_favicon.png" pelo nome do seu arquivo
except FileNotFoundError:
    st.error("Arquivo não encontrado.")
    img = None # Define img como None se o arquivo não for encontrado

# 2. Configurar a página com o favicon
if img:
    st.set_page_config(
        page_title="Sistema de Gestão de Notas Fiscais por PO",
        page_icon=img, # Usa o objeto de imagem
        initial_sidebar_state="collapsed",
        layout="wide"
    )
else:
    # Se a imagem não for encontrada, usa um ícone padrão ou texto
    st.set_page_config(
        page_title="Sistema de Gestão de Notas Fiscais por PO",
        page_icon="📄", # Exemplo de um ícone de texto
        initial_sidebar_state="collapsed",
        layout="wide"
    )

st.title("📄 Sistema de Gestão de Notas Fiscais por PO")

# Load data
df_fornecedores = load_suppliers()
df_pos = load_pos()
df_notas = load_notes()

# Sidebar
df_fornecedores, df_pos = render_sidebar(df_fornecedores, df_pos)

# Main content
st.header("Gestão de Notas Fiscais")
col1, col2 = st.columns([1, 3])

with col1:
    df_pos, df_notas = render_notes_form(df_pos, df_notas)

with col2:
    df_filtrado = render_notes_table(df_notas)

    # Supplier-month pivot below table
    render_supplier_month_pivot(df_filtrado.copy() if df_filtrado is not None else df_notas.copy())

    st.write("### Selecione uma Nota Fiscal")
    copiado = False
    if not df_filtrado.empty:
        notas_options = {
            f"{row['nota_numero']} - {row['descricao']}": row
            for _, row in df_filtrado.iterrows()
        }

    # Cria uma lista com a opção "Selecione..."
    opcoes = [""] + list(notas_options.keys())

    nota_selecionada = st.selectbox(
        "Selecione ou digite a Nota Fiscal:",
        options=opcoes,
        index=0,  # começa vazio
        format_func=lambda x: "" if x == "" else x
    )

    if nota_selecionada != "":
        colBut1, colBut2 = st.columns([1, 4])
        with colBut1:
            if st.button("📋 Copiar Dados da Nota"):
                copy_invoice_message(df_pos, notas_options[nota_selecionada])
                copiado = True
        with colBut2:
            if st.button("🔗 Copiar PO e Acessar Site"):
                copy_po(notas_options[nota_selecionada])
                copiado = True
                st.markdown(
                    f'<meta http-equiv="refresh" content="0;URL=https://mysapportal.volvocars.net/irj/portal?NavigationTarget=navurl%3A%2F%2Fb651e43fa7c1f266b577b26a1a733937&ExecuteLocally=true&CurrentWindowId=WID1741872159289&supportInitialNavNodesFilter=true&PrevNavTarget=navurl%3A%2F%2F36dc7541f22586542f28b96f9767585d&NavMode=3">',
                    unsafe_allow_html=True
                )


        if copiado:
            st.write("")
            st.success("Dados copiados para a área de transferência!")

# Analytics
render_analytics(df_pos, df_notas, df_filtrado if 'df_filtrado' in locals() else df_notas)

# Records management
df_pos, df_notas = render_records_manager(df_pos, df_notas)

