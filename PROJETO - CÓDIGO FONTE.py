import sqlite3
import pandas as pd
from datetime import datetime

def registrar_log(mensagem):
    with open("log.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{datetime.now()} - {mensagem}\n")

try:

    registrar_log("Iniciando integração")

    conexao_origem = sqlite3.connect("origem.db")

    consulta = "SELECT * FROM usuarios"

    dados = pd.read_sql_query(
        consulta,
        conexao_origem
    )

    if dados.empty:
        raise Exception("Nenhum registro encontrado")

    registrar_log(
        f"{len(dados)} registros encontrados"
    )

    dados.columns = [
        "codigo",
        "nome_completo",
        "email",
        "idade"
    ]

    dados["nome_completo"] = (
        dados["nome_completo"]
        .str.upper()
    )

    conexao_destino = sqlite3.connect(
        "destino.db"
    )

    dados.to_sql(
        "clientes",
        conexao_destino,
        if_exists="replace",
        index=False
    )

    conexao_origem.close()
    conexao_destino.close()

    registrar_log(
        "Integração concluída com sucesso"
    )

    print("Processo finalizado")

except Exception as erro:

    registrar_log(f"Erro: {erro}")

    print(f"Erro durante integração: {erro}")