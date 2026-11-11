from sqlite3 import OperationalError

from helpers.database import get_connection
from helpers.file.json import read, write
from models.instituicaoensino import InstituicaoEnsino

ARQUIVO_JSON = "instituicoes.json"


class InstituicaoEnsinoRepository():

    def row_to_instituicao(self, row):
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

    def getInstituicoes(self, page=1, limit=100):
        connection = get_connection()
        try:
            offset = (page - 1) * limit
            cursor = connection.cursor()
            cursor.execute("""
                SELECT id, no_entidade, co_entidade, no_uf, sg_uf, co_uf, no_municipio, co_municipio, nu_ano_censo, qt_mat_bas, qt_mat_inf,
                    qt_mat_fund, qt_mat_med, qt_mat_prof, qt_mat_eja, qt_mat_esp, created_at
                FROM tb_instituicao_ensino
                WHERE deleted_at IS NULL
                LIMIT ? OFFSET ?
            """, (limit, offset))
            rows = cursor.fetchall()

            instituicoes = [
                self.row_to_instituicao(row)
                for row in rows
            ]
        except OperationalError:
            connection.rollback()
            raise

        return instituicoes

    def getInstituicao(self, id):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT id, no_entidade, co_entidade, no_uf, sg_uf, co_uf, no_municipio, co_municipio, nu_ano_censo, qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med, qt_mat_prof, qt_mat_eja, qt_mat_esp, created_at
                FROM tb_instituicao_ensino
                WHERE id = ? AND deleted_at IS NULL
            """, (id,))
            row = cursor.fetchone()

            if row is None:
                return None

            instituicao = self.row_to_instituicao(row)

        except OperationalError:
            connection.rollback()
            raise

        return instituicao

    def createInstituicao(self, data):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO tb_instituicao_ensino (no_entidade, co_entidade, no_uf, sg_uf, co_uf, no_municipio, co_municipio, nu_ano_censo, qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med, qt_mat_prof, qt_mat_eja, qt_mat_esp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                RETURNING id, created_at
            """, (
                data["no_entidade"], data["co_entidade"], data["no_uf"], data["sg_uf"], data["co_uf"], data["no_municipio"], data["co_municipio"],
                data["nu_ano_censo"], data["qt_mat_bas"], data["qt_mat_inf"], data["qt_mat_fund"], data["qt_mat_med"], data["qt_mat_prof"], data["qt_mat_eja"], data["qt_mat_esp"]
            ))

            resultset = cursor.fetchone()
            id = resultset[0]
            created = resultset[1]

            connection.commit()

            return InstituicaoEnsino(**data, id=id, created=created)
        except OperationalError:
            connection.rollback()
            raise

    def updateInstituicao(self, id, data):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE tb_instituicao_ensino
                SET no_entidade = ?, co_entidade = ?, no_uf = ?, sg_uf = ?, co_uf = ?, no_municipio = ?, co_municipio = ?,
                    nu_ano_censo = ?, qt_mat_bas = ?, qt_mat_inf = ?, qt_mat_fund = ?, qt_mat_med = ?, qt_mat_prof = ?, qt_mat_eja = ?, qt_mat_esp = ?
                WHERE id = ? AND deleted_at IS NULL
            """, (
                data["no_entidade"], data["co_entidade"], data["no_uf"], data["sg_uf"], data["co_uf"], data["no_municipio"], data["co_municipio"],
                data["nu_ano_censo"], data["qt_mat_bas"], data["qt_mat_inf"], data["qt_mat_fund"], data["qt_mat_med"], data["qt_mat_prof"], data["qt_mat_eja"], data["qt_mat_esp"],
                id
            ))

            if cursor.rowcount == 0:
                return None

            connection.commit()
            return self.getInstituicao(id)
        except OperationalError:
            connection.rollback()
            raise

    def deleteInstituicao(self, id):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE tb_instituicao_ensino
                SET deleted_at = CURRENT_TIMESTAMP
                WHERE id = ? AND deleted_at IS NULL
            """, (id,))

            if cursor.rowcount == 0:
                return False

            connection.commit()
            return True
        except OperationalError:
            connection.rollback()
            raise

    def getInstituicoesJson(self):
        return read(ARQUIVO_JSON)

    def getInstituicaoJson(self, id):
        dataset = read(ARQUIVO_JSON)
        for item in dataset:
            if str(item.get("id")) == str(id):
                return item
        return None

    def createInstituicaoJson(self, data):
        dataset = read(ARQUIVO_JSON)
        novo_id = 1
        if len(dataset) > 0:
            novo_id = max(int(item["id"]) for item in dataset) + 1
        novo = {"id": str(novo_id), **data}
        dataset.append(novo)
        write(ARQUIVO_JSON, dataset)
        return novo

    def updateInstituicaoJson(self, id, data):
        dataset = read(ARQUIVO_JSON)
        for i, item in enumerate(dataset):
            if str(item.get("id")) == str(id):
                atualizado = {"id": str(id), **data}
                dataset[i] = atualizado
                write(ARQUIVO_JSON, dataset)
                return atualizado
        return None

    def deleteInstituicaoJson(self, id):
        dataset = read(ARQUIVO_JSON)
        for i, item in enumerate(dataset):
            if str(item.get("id")) == str(id):
                dataset.pop(i)
                write(ARQUIVO_JSON, dataset)
                return True
        return False
