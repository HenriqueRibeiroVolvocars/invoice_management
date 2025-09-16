import streamlit as st
import pandas as pd
from .data import save_data
from .services import update_po_balance


def render_notes_form(df_pos: pd.DataFrame, df_notas: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    with st.form("nova_nota_form"):
        st.subheader("Lançar Nova Nota")

        po_selecionada = st.selectbox("Selecionar PO*", options=df_pos["descricao"]) if not df_pos.empty else None
        if po_selecionada is None:
            st.info("Cadastre uma PO para lançar notas.")
            return df_pos, df_notas

        po_code = df_pos[df_pos["descricao"] == po_selecionada]["po_code"].values[0]
        saldo_po = df_pos[df_pos["descricao"] == po_selecionada]["saldo_disponivel"].values[0]

        if st.form_submit_button("Exibir mais informações"):
            fornecedor_info = df_pos[df_pos["descricao"] == po_selecionada]["fornecedor"].values[0]
            st.metric("Saldo Disponível na PO", f"R$ {saldo_po:,.2f}")
            st.metric("Fornecedor", fornecedor_info)

        nota_numero = st.text_input("Número da Nota*")
        descricao_nota = st.text_input("Descrição da Nota*")
        valor_nota = st.number_input("Valor (R$)*", min_value=0.0, max_value=saldo_po if not df_pos.empty else None)
        data_emissao = st.date_input("Data de Emissão*")
        data_vencimento = st.date_input("Data de Vencimento*")
        status_pagamento = st.selectbox("Status*", ["Pendente", "Pago", "Cancelado"])
        codigo_for = df_pos[df_pos["descricao"] == po_selecionada]["codigo_for"].values[0] if "codigo_for" in df_pos.columns else ""
        fornecedor = df_pos[df_pos["descricao"] == po_selecionada]["fornecedor"].values[0]

        if st.form_submit_button("Registrar Nota"):
            if not all([nota_numero, descricao_nota, valor_nota]):
                st.error("Campos obrigatórios (*) devem ser preenchidos!")
            else:
                nova_nota = pd.DataFrame([{
                    "nota_numero": nota_numero,
                    "po_code": po_code,
                    "descricao": descricao_nota,
                    "valor": valor_nota,
                    "data_emissao": pd.to_datetime(data_emissao),
                    "data_vencimento": pd.to_datetime(data_vencimento),
                    "status_pagamento": status_pagamento,
                    "fornecedor": fornecedor,
                    "codigo_for": codigo_for
                }])

                df_notas = pd.concat([df_notas, nova_nota], ignore_index=True)
                save_data(df_notas, "notas")

                update_po_balance(df_pos, df_notas, po_code)
                st.success("Nota registrada com sucesso!")

    return df_pos, df_notas

