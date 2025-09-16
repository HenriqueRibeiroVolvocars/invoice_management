import pandas as pd
import pyperclip
from datetime import datetime
from .data import save_data


def update_po_balance(df_pos: pd.DataFrame, df_notas: pd.DataFrame, po_code: str) -> None:
    valor_utilizado = df_notas[df_notas["po_code"] == po_code]["valor"].sum()
    df_pos.loc[df_pos["po_code"] == po_code, "valor_utilizado"] = valor_utilizado
    df_pos.loc[df_pos["po_code"] == po_code, "saldo_disponivel"] = (
        df_pos.loc[df_pos["po_code"] == po_code, "valor_total"] - valor_utilizado
    )
    save_data(df_pos, "pos")


def copy_invoice_message(df_pos: pd.DataFrame, row: pd.Series) -> None:
    codigo_for = df_pos[df_pos["po_code"] == row["po_code"]]["codigo_for"].values[0] if row["po_code"] in df_pos["po_code"].values else ""
    conta_contabil = df_pos[df_pos["po_code"] == row["po_code"]]["conta_contabil"].values[0] if row["po_code"] in df_pos["po_code"].values else ""
    centro_custo = df_pos[df_pos["po_code"] == row["po_code"]]["centro_custo"].values[0] if row["po_code"] in df_pos["po_code"].values else ""
    forma_pagamento = df_pos[df_pos["po_code"] == row["po_code"]]["forma_pagamento"].values[0] if row["po_code"] in df_pos["po_code"].values else ""
    banco = df_pos[df_pos["po_code"] == row["po_code"]]["banco"].values[0] if row["po_code"] in df_pos["po_code"].values else ""
    agencia = df_pos[df_pos["po_code"] == row["po_code"]]["agencia"].values[0] if row["po_code"] in df_pos["po_code"].values else ""
    cc = df_pos[df_pos["po_code"] == row["po_code"]]["cc"].values[0] if row["po_code"] in df_pos["po_code"].values else ""

    data_tr = datetime.strftime(row["data_vencimento"], "%d/%m/%Y") if not pd.isnull(row["data_vencimento"]) else ""
    dados_nf = (
        f"Boa tarde,\n"
        f"Tudo bem?.\n"
        f"Vocês poderiam efetuar esse pagamento? Segue abaixo solicitação e aprovação.\n"
        f"Em anexo, a NF.\n"
        f"\n"
        f"Solicitação de Pagamento – {row['descricao']} - {data_tr}\n"
        f"PO/FB60: {row['po_code']}\n"
        f"Código Fornecedor: {codigo_for}\n"
        f"Nº Documento Fiscal/ND: {row['nota_numero']}\n"
        f"MIGO: \n"
        f"Descrição: {row['descricao']}\n"
        f"Valor Bruto: R$ {row['valor']:.2f}\n"
        f"Conta Contábil: {conta_contabil}\n"
        f"Centro de Custo: {centro_custo}\n"
        f"Forma de Pagamento: {forma_pagamento}\n"
        f"Banco: {banco}\n"
        f"Agencia: {agencia}\n"
        f"C/C: {cc}"
        f"\n"
        f"Att\n"
    )
    pyperclip.copy(dados_nf)


def copy_po(row: pd.Series) -> None:
    pyperclip.copy(f"{row['po_code']}")

