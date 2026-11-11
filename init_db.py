import sqlite3
import json
from helpers.enviroment import enviroment

DATABASE = enviroment.get("DB_NAME", "censoescolar.db")

connection = None

try:
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS tb_instituicao_ensino;")

    with open('schema.sql', encoding='utf-8') as file:
        connection.executescript(file.read())

    with open('instituicoes.json', 'r', encoding='utf-8') as f:
        instituicoes = json.load(f)

    registros = [
        (
            item["no_entidade"],
            str(item["co_entidade"]),
            item["no_uf"],
            item["sg_uf"],
            int(item["co_uf"]),
            item["no_municipio"],
            int(item["co_municipio"]),
            int(item["nu_ano_censo"]),
            int(item["qt_mat_bas"]),
            int(item["qt_mat_inf"]),
            int(item["qt_mat_fund"]),
            int(item["qt_mat_med"]),
            int(item["qt_mat_prof"]),
            int(item["qt_mat_eja"]),
            int(item["qt_mat_esp"])
        )
        for item in instituicoes
    ]

    cursor.executemany("""
        INSERT INTO tb_instituicao_ensino (
            no_entidade, co_entidade, no_uf, sg_uf, co_uf,
            no_municipio, co_municipio, nu_ano_censo,
            qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med,
            qt_mat_prof, qt_mat_eja, qt_mat_esp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, registros)

    connection.commit()
    print(f"Banco inicializado e {len(registros)} instituições migradas do JSON com sucesso.")
except sqlite3.Error as e:
    print(f'O sqlite lançou uma exceção: {str(e)}')
finally:
    if connection is not None:
        connection.close()
