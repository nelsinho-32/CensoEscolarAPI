from helpers.database import get_connection
from helpers.logger import logger

from repositories.InstituicaoEnsinoRepository import InstituicaoEnsinoRepository


class InstituicaoEnsinoService():
    def __init__(self):
        self.instituicaoEnsinoRepository = InstituicaoEnsinoRepository()

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

    def get_by_id(self, id):
        return self.instituicaoEnsinoRepository.getInstituicao(id)
