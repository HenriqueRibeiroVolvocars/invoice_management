import streamlit as st
import pandas as pd
from .data import save_data


def render_sidebar(df_fornecedores: pd.DataFrame, df_pos: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    with st.sidebar:
        st.header("Cadastros Básicos")
        tab_forn, tab_po = st.tabs(["Fornecedor", "PO"])

        with tab_forn:
            st.subheader("Novo Fornecedor")
            cnpj = st.text_input("CNPJ")
            razao_social = st.text_input("Razão Social")
            nome_fantasia = st.text_input("Nome Fantasia")

            if st.button("Salvar Fornecedor"):
                novo_fornecedor = pd.DataFrame([[cnpj, razao_social, nome_fantasia]],
                                             columns=["cnpj", "razao_social", "nome_fantasia"])
                df_fornecedores = pd.concat([df_fornecedores, novo_fornecedor], ignore_index=True)
                save_data(df_fornecedores, "fornecedores")
                st.success("Fornecedor cadastrado!")

        with tab_po:
            st.subheader("Nova PO")
            po_code = st.text_input("Código da PO*")
            descricao_po = st.text_input("Descrição da PO*")
            fornecedor_po = st.selectbox("Fornecedor*", options=df_fornecedores["nome_fantasia"].unique())
            valor_total = st.number_input("Valor Total Contratado (R$)*", min_value=0.0)

            if st.button("Criar PO"):
                nova_po = pd.DataFrame([[po_code, descricao_po, fornecedor_po, valor_total, 0, valor_total, pd.Timestamp.today()]],
                                     columns=["po_code", "descricao", "fornecedor", "valor_total",
                                              "valor_utilizado", "saldo_disponivel", "data_abertura"])
                df_pos = pd.concat([df_pos, nova_po], ignore_index=True)
                save_data(df_pos, "pos")
                st.success("PO cadastrada com sucesso!")

    return df_fornecedores, df_pos

