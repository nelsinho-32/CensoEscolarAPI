from flask import Blueprint, request, jsonify
from sqlite3 import OperationalError
from marshmallow import ValidationError

from models.instituicaoensino import InstituicaoEnsino, InstituicaoEnsinoSchema, InstituicaoEnsinoCompactoSchema
from services.InstituicaoEnsinoService import InstituicaoEnsinoService
from helpers.database import get_connection
from helpers.logger import logger

from services.InstituicaoEnsinoService import InstituicaoEnsinoService

instituicaoEnsinoSchema = InstituicaoEnsinoSchema()
instituicoesEnsinoSchema = InstituicaoEnsinoSchema(many=True)
instituicaoEnsinoCompactoSchema = InstituicaoEnsinoCompactoSchema(many=True)


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


instituicao_ensino_bp = Blueprint(
    'instituicaoensino', __name__, url_prefix='/instituicoesensino')


@instituicao_ensino_bp.get("/")
def get_all_instituicoes():

    logger.info("Listando as Insituições de Ensino")

    instituicaoEnsinoService = InstituicaoEnsinoService()
    instituicoes = instituicaoEnsinoService.get_all()
    logger.info("Finalizando o processamento da Listagem")
    return jsonify(instituicoesEnsinoSchema.dump(instituicoes)), 200


@instituicao_ensino_bp.get("/<int:id>")
def get_instituicao_by_id(id):
    try:
        service = InstituicaoEnsinoService()
        instituicaoEnsino = service.get_by_id(id)
        if instituicaoEnsino is None:
            return {
                "mensagem": "Instituição de ensino não encontrada"
            }, 404
        return jsonify(instituicaoEnsinoSchema.dump(instituicaoEnsino)), 200
    except OperationalError:
        return {
            "mensagem": "Problema ao estabelecer a "
        }, 500


@instituicao_ensino_bp.post("/")
def post_instituicao():

    try:
        data = InstituicaoEnsinoSchema.load(request.get_json())

        connection = get_connection()

        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO tb_instituicao_ensino (no_entidade, co_entidade, no_uf, sg_uf, co_uf, no_municipio, co_municipio, nu_ano_censo, qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med, qt_mat_prof, qt_mat_eja, qt_mat_esp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            RETURNING id, created
        """, (
            data["no_entidade"], data["co_entidade"], data["no_uf"], data["sg_uf"], data["co_uf"], data["no_municipio"], data["co_municipio"], data["nu_ano_censo"], data[
                "qt_mat_bas"], data["qt_mat_inf"], data["qt_mat_fund"], data["qt_mat_med"], data["qt_mat_prof"], data["qt_mat_eja"], data["qt_mat_esp"]
        ))

        resultset = cursor.fetchone()
        id = resultset[0]
        created = resultset[1]

        connection.commit()

        instituicao = InstituicaoEnsino(**data, id=id, created=created)

        return jsonify(instituicaoEnsinoSchema.dump(instituicao)), 201

    except ValidationError as err:

        return {"erro": "Dados inválidos", "campos": err.messages}, 400

    except OperationalError:
        connection.rollback()
        raise


@instituicao_ensino_bp.put("/<int:id>")
def putInstituicoes():
    pass


@instituicao_ensino_bp.delete("/<int:id>")
def deleteInstituicoes():
    pass
