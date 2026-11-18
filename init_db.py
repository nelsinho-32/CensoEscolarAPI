import os
import json
import psycopg2
from helpers.enviroment import enviroment

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(BASE_DIR, 'schema.sql')
INSTITUICOES_JSON_PATH = os.path.join(BASE_DIR, 'instituicoes.json')


def init_db():
    host = enviroment.get("DB_HOST", "localhost")
    port = int(enviroment.get("DB_PORT", 5435))
    dbname = enviroment.get("DB_NAME", "censoescolar")
    user = enviroment.get("DB_USER", "postgres")
    password = enviroment.get("DB_PASSWORD", "123456")

    connection = None
    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        cursor = connection.cursor()


        if os.path.exists(SCHEMA_PATH):
            with open(SCHEMA_PATH, encoding='utf-8') as file:
                cursor.execute(file.read())

        registros = []
        if os.path.exists(INSTITUICOES_JSON_PATH):
            with open(INSTITUICOES_JSON_PATH, 'r', encoding='utf-8') as f:
                instituicoes = json.load(f)

            registros = [
                (
                    item.get("no_entidade"),
                    str(item.get("co_entidade")),
                    item.get("no_uf"),
                    item.get("sg_uf"),
                    int(item.get("co_uf", 0)),
                    item.get("no_municipio"),
                    int(item.get("co_municipio", 0)),
                    int(item.get("nu_ano_censo", 2025)),
                    int(item.get("qt_mat_bas", 0)),
                    int(item.get("qt_mat_inf", 0)),
                    int(item.get("qt_mat_fund", 0)),
                    int(item.get("qt_mat_med", 0)),
                    int(item.get("qt_mat_prof", 0)),
                    int(item.get("qt_mat_eja", 0)),
                    int(item.get("qt_mat_esp", 0))
                )
                for item in instituicoes
            ]

            if registros:
                cursor.executemany("""
                    INSERT INTO tb_instituicao_ensino (
                        no_entidade, co_entidade, no_uf, sg_uf, co_uf,
                        no_municipio, co_municipio, nu_ano_censo,
                        qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med,
                        qt_mat_prof, qt_mat_eja, qt_mat_esp
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    ON CONFLICT (co_entidade) DO NOTHING
                """, registros)

        connection.commit()
        print(f"Banco inicializado e {len(registros)} instituições migradas com sucesso.")

    except psycopg2.Error as e:
        if connection:
            connection.rollback()
        print(f"Erro ao conectar ou executar no PostgreSQL: {e}")
    finally:
        if connection is not None and not connection.closed:
            connection.close()


if __name__ == '__main__':
    init_db()
