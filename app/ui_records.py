import streamlit as st
import pandas as pd
from .data import save_data
from .services import update_po_balance


def render_records_manager(df_pos: pd.DataFrame, df_notas: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    st.header("Gestão de Registros")
    with st.expander("Editar/Excluir Notas"):
        if not df_notas.empty:
            nota_selecionada = st.selectbox("Selecionar Nota", df_notas["nota_numero"])            
            nota_data = df_notas[df_notas["nota_numero"] == nota_selecionada].iloc[0]
            po_relacionada = nota_data["po_code"]

            col_edit1, col_edit2 = st.columns(2)
            with col_edit1:
                novo_status = st.selectbox(
                    "Status",
                    options=["Pendente", "Pago", "Cancelado"],
                    index=["Pendente", "Pago", "Cancelado"].index(nota_data["status_pagamento"])
                )
            with col_edit2:
                max_value = (df_pos["saldo_disponivel"].values[0] + nota_data["valor"]) if not df_pos.empty else None
                novo_valor = st.number_input("Valor", value=nota_data["valor"], max_value=max_value)

            if st.button("Atualizar Nota"):
                diferenca_valor = novo_valor - nota_data["valor"]
                if diferenca_valor != 0:
                    df_notas.loc[df_notas["nota_numero"] == nota_selecionada, "valor"] = novo_valor
                    update_po_balance(df_pos, df_notas, po_relacionada)

                df_notas.loc[df_notas["nota_numero"] == nota_selecionada, "status_pagamento"] = novo_status
                save_data(df_notas, "notas")
                st.success("Nota atualizada com sucesso!")
                st.experimental_rerun()

            if st.button("Excluir Nota", type="primary"):
                df_notas = df_notas[df_notas["nota_numero"] != nota_selecionada]
                save_data(df_notas, "notas")
                update_po_balance(df_pos, df_notas, po_relacionada)
                st.success("Nota excluída com sucesso!")
                st.experimental_rerun()
        else:
            st.warning("Nenhuma nota disponível para edição")

    return df_pos, df_notas

