import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def render_analytics(df_pos: pd.DataFrame, df_notas: pd.DataFrame, df_filtrado: pd.DataFrame) -> None:
    st.header("Análises Financeiras")
    col_analise1, col_analise2, col_analise3 = st.columns(3)

    with col_analise1:
        st.subheader("Status de Pagamento")
        if not df_notas.empty:
            fig = plt.figure(figsize=(2, 6))
            df_notas["status_pagamento"].value_counts().plot.pie(
                autopct="%1.1f%%", startangle=90, colors=["#ff9999", "#66b3ff", "#99ff99"]
            )
            plt.title("Status de Pagamento")
            st.pyplot(fig)
        else:
            st.warning("Nenhuma nota registrada para análise")

    with col_analise2:
        st.subheader("Gastos Mensais por Fornecedor")
        if not df_notas.empty:
            fig, ax = plt.subplots(figsize=(12, 9))
            df_notas["data"] = pd.to_datetime(df_notas["data_emissao"])
            df_notas["mes_ano"] = df_notas["data_emissao"].dt.to_period("M").astype(str)

            df_pivot = df_notas.groupby(["mes_ano", "fornecedor"])["valor"].sum().unstack(fill_value=0)

            if not df_pivot.empty:
                df_pivot.plot(kind="line", marker="o", ax=ax, colormap="tab10")

                ax.set_title("Gastos Mensais por Fornecedor")
                ax.set_xlabel("Mês")
                ax.set_ylabel("Valor Total")
                ax.set_xticks(range(len(df_pivot.index)))
                ax.set_xticklabels(df_pivot.index, rotation=45)
                ax.legend(title="Fornecedores", bbox_to_anchor=(1.05, 1), loc="upper left")
                plt.grid(True, linestyle="--", alpha=0.7)
                plt.tight_layout()

                st.pyplot(fig)
            else:
                st.warning("Nenhum dado disponível para gerar o gráfico.")
        else:
            st.warning("Nenhuma nota registrada para análise.")

    with col_analise3:
        st.subheader("Status das POs e Resumo Financeiro")
        if not df_pos.empty:
            fig, ax = plt.subplots(figsize=(8, 6))

            total_gastos = df_pos["valor_utilizado"].sum()
            saldo_atual = df_pos["saldo_disponivel"].sum()
            diferenca = saldo_atual - total_gastos

            df_financeiro = pd.DataFrame({
                "Categoria": ["Gastos Totais", "Saldo Atual das POs", "Diferença"],
                "Valor": [total_gastos, saldo_atual, diferenca]
            })

            bars = ax.bar(df_financeiro["Categoria"], df_financeiro["Valor"], color=["blue", "orange", "gray"])

            for bar in bars:
                yval = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, yval, f'R$ {yval:,.2f}', ha='center', va='bottom', fontsize=10)

            ax.set_title("Gastos Totais vs Saldo Atual das POs e Diferença")
            ax.set_ylabel("Valor")
            ax.set_xlabel("Categorias")
            plt.tight_layout()

            st.pyplot(fig)
        else:
            st.warning("Nenhuma PO cadastrada")


def render_supplier_month_pivot(df_filtrado: pd.DataFrame) -> None:
    df_filtrado['data_vencimento'] = pd.to_datetime(df_filtrado['data_vencimento'])
    df_filtrado['mes_num'] = df_filtrado['data_vencimento'].dt.month
    df_filtrado['ano'] = df_filtrado['data_vencimento'].dt.year

    meses_map = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
        5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
        9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }

    df_filtrado['mês'] = df_filtrado['mes_num'].map(meses_map)
    df_filtrado = df_filtrado.sort_values(by=['ano', 'mes_num'])

    pivot = pd.pivot_table(
        df_filtrado,
        index='fornecedor',
        columns='mês',
        values='valor',
        aggfunc='sum',
        fill_value=0
    )

    meses_ordem = [meses_map[i] for i in range(1, 13) if meses_map[i] in pivot.columns]
    pivot = pivot[meses_ordem]
    pivot['Total Anual'] = pivot.sum(axis=1)

    totais_mensais = pivot.sum().to_frame().T
    totais_mensais.index = ['Total Mensal']

    pivot = pivot.reset_index()
    pivot_final = pd.concat([pivot, totais_mensais], ignore_index=True)

    st.dataframe(pivot_final, use_container_width=True)

