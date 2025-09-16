import pandas as pd
from datetime import datetime


def load_suppliers() -> pd.DataFrame:
    try:
        return pd.read_excel("fornecedores.xlsx")
    except FileNotFoundError:
        return pd.DataFrame(columns=["cnpj", "razao_social", "nome_fantasia"])


def load_pos() -> pd.DataFrame:
    try:
        df = pd.read_csv("pos.csv")
        if "data_abertura" in df.columns:
            df["data_abertura"] = pd.to_datetime(df["data_abertura"])
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=[
            "po_code", "descricao", "fornecedor", "valor_total",
            "valor_utilizado", "saldo_disponivel", "data_abertura", "conta_contabil"
        ])


def load_notes() -> pd.DataFrame:
    try:
        return pd.read_csv("notas.csv", parse_dates=["data_emissao", "data_vencimento"])
    except FileNotFoundError:
        return pd.DataFrame(columns=[
            "nota_numero", "po_code", "descricao", "valor",
            "data_emissao", "data_vencimento", "status_pagamento", "fornecedor", "codigo_for"
        ])


def save_data(df: pd.DataFrame, kind: str) -> None:
    if kind == "pos":
        df.to_csv("pos.csv", index=False)
    elif kind == "notas":
        df.to_csv("notas.csv", index=False)
    elif kind == "fornecedores":
        df.to_excel("fornecedores.xlsx", index=False)


def create_po_row(po_code: str, descricao: str, fornecedor: str, valor_total: float) -> pd.DataFrame:
    return pd.DataFrame([[po_code, descricao, fornecedor, valor_total, 0, valor_total, datetime.today()]],
                        columns=["po_code", "descricao", "fornecedor", "valor_total",
                                 "valor_utilizado", "saldo_disponivel", "data_abertura"]) 

