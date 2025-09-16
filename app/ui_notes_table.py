import streamlit as st
import pandas as pd
from datetime import datetime


def render_notes_table(df_notas: pd.DataFrame) -> pd.DataFrame:
    st.subheader("Notas Registradas")

    cols_filtro = st.columns(4)
    with cols_filtro[0]:
        filtro_po = st.selectbox("Filtrar por PO", ["Todas"] + list(df_notas["po_code"].unique())) if not df_notas.empty else "Todas"
    with cols_filtro[1]:
        filtro_status = st.selectbox("Filtrar por Status", ["Todos"] + list(df_notas["status_pagamento"].unique())) if not df_notas.empty else "Todos"
    with cols_filtro[2]:
        filtro_forn = st.selectbox("Filtrar por Fornecedor", ["Todos"] + list(df_notas["fornecedor"].unique())) if not df_notas.empty else "Todos"
    with cols_filtro[3]:
        busca = st.text_input("Buscar por descrição Nota")

    cols_data = st.columns(2)
    with cols_data[0]:
        data_inicio = st.date_input("Data de emissão - Início", value=None)
    with cols_data[1]:
        data_fim = st.date_input("Data de emissão - Fim", value=None)

    df_filtrado = df_notas.copy()
    if not df_filtrado.empty:
        if filtro_po != "Todas":
            df_filtrado = df_filtrado[df_filtrado["po_code"] == filtro_po]
        if filtro_status != "Todos":
            df_filtrado = df_filtrado[df_filtrado["status_pagamento"] == filtro_status]
        if filtro_forn != "Todos":
            df_filtrado = df_filtrado[df_filtrado["fornecedor"] == filtro_forn]
        if busca:
            df_filtrado = df_filtrado[df_filtrado.apply(
                lambda row: busca.lower() in str(row["nota_numero"]).lower() or busca.lower() in row["descricao"].lower(), axis=1)]

        if data_inicio:
            df_filtrado = df_filtrado[df_filtrado["data_emissao"] >= pd.to_datetime(data_inicio)]
        if data_fim:
            df_filtrado = df_filtrado[df_filtrado["data_emissao"] <= pd.to_datetime(data_fim)]

        st.dataframe(df_filtrado[['nota_numero', 'po_code', 'fornecedor', 'descricao', 'valor', 'data_emissao', 'data_vencimento',
                                  'status_pagamento', 'codigo_for']], use_container_width=True)

        data_f = datetime.today().strftime('%Y%m%d')
        output_file = f"{data_f}_FX_NFs.xlsx"
        df_filtrado.to_excel(output_file, index=False)

        with open(output_file, "rb") as file:
            st.download_button(
                label="Baixar Arquivo Processado",
                data=file,
                file_name=output_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    return df_filtrado

