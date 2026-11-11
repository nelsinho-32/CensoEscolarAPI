from flask import Blueprint, request, jsonify
from sqlite3 import OperationalError
from marshmallow import ValidationError

from models.instituicaoensino import InstituicaoEnsinoSchema, InstituicaoEnsinoCompactoSchema
from services.InstituicaoEnsinoService import InstituicaoEnsinoService
from helpers.logger import logger

instituicaoEnsinoSchema = InstituicaoEnsinoSchema()
instituicoesEnsinoSchema = InstituicaoEnsinoSchema(many=True)
instituicaoEnsinoCompactoSchema = InstituicaoEnsinoCompactoSchema(many=True)

instituicao_ensino_bp = Blueprint(
    'instituicaoensino', __name__, url_prefix='/instituicoesensino')


@instituicao_ensino_bp.get("/")
def get_all_instituicoes():
    logger.info("Listando as Instituições de Ensino")
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 100, type=int)

    instituicaoEnsinoService = InstituicaoEnsinoService()
    instituicoes = instituicaoEnsinoService.get_all(page, limit)
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
            "mensagem": "Problema ao estabelecer a conexão com o banco de dados"
        }, 500


@instituicao_ensino_bp.post("/")
def post_instituicao():
    try:
        data = instituicaoEnsinoSchema.load(request.get_json())
        service = InstituicaoEnsinoService()
        instituicao = service.create(data)
        return jsonify(instituicaoEnsinoSchema.dump(instituicao)), 201
    except ValidationError as err:
        return {"erro": "Dados inválidos", "campos": err.messages}, 400
    except OperationalError:
        return {
            "mensagem": "Problema ao salvar no banco de dados"
        }, 500


@instituicao_ensino_bp.put("/<int:id>")
def putInstituicoes(id):
    try:
        data = instituicaoEnsinoSchema.load(request.get_json())
        service = InstituicaoEnsinoService()
        instituicao = service.update(id, data)
        if instituicao is None:
            return {
                "mensagem": "Instituição de ensino não encontrada"
            }, 404
        return jsonify(instituicaoEnsinoSchema.dump(instituicao)), 200
    except ValidationError as err:
        return {"erro": "Dados inválidos", "campos": err.messages}, 400
    except OperationalError:
        return {
            "mensagem": "Problema ao atualizar no banco de dados"
        }, 500


@instituicao_ensino_bp.delete("/<int:id>")
def deleteInstituicoes(id):
    try:
        service = InstituicaoEnsinoService()
        removido = service.delete(id)
        if not removido:
            return {
                "mensagem": "Instituição de ensino não encontrada"
            }, 404
        return {
            "mensagem": "Instituição de ensino removida com sucesso"
        }, 200
    except OperationalError:
        return {
            "mensagem": "Problema ao remover no banco de dados"
        }, 500
