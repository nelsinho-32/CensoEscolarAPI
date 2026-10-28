from helpers.database import get_connection
from helpers.logger import logger

from models.instituicaoensino import InstituicaoEnsino, InstituicaoEnsinoSchema, InstituicaoEnsinoCompactoSchema


class InstituicaoEnsinoService():
    def __init__(self):
        pass

    def row_to_instituicao(row):
        return InstituicaoEnsino(
            id=row[0],
            no_entidade=row[1],
            co_entidade=row[2],
            no_uf=row[3],
            sg_uf=row[4],
            co_uf=row[5],
            no_municipio=row[6],
            co_municipio=row[7],
            nu_ano_censo=row[8],
            qt_mat_bas=row[9],
            qt_mat_inf=row[10],
            qt_mat_fund=row[11],
            qt_mat_med=row[12],
            qt_mat_prof=row[13],
            qt_mat_eja=row[14],
            qt_mat_esp=row[15],
            created=row[16]
        )

    def get_all():
        connection = get_connection()
        try:
            logger.info("Recuperando a conexão com o Banco de dados")
            cursor = connection.cursor()
            cursor.execute("""
            SELECT id, no_entidade, co_entidade, no_uf, sg_uf, co_uf, no_municipio, co_municipio, nu_ano_censo, qt_mat_bas, qt_mat_inf,
                qt_mat_fund, qt_mat_med, qt_mat_prof, qt_mat_eja, qt_mat_esp, created
            FROM tb_instituicao_ensino
        """)
            rows = cursor.fetchall()

            instituicoes = [
                row_to_instituicao(row)
                for row in rows
            ]
        except OperationalError:
            logger.error("Erro no processamento dos dados no Banco de Dados")
            connection.rollback()
            raise

        return instituicoes
