from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from models.instituicaoensino import InstituicaoEnsinoSchema
from services.InstituicaoEnsinoService import InstituicaoEnsinoService

instituicaoEnsinoSchema = InstituicaoEnsinoSchema()

instituicao_json_bp = Blueprint(
    'instituicoes_json', __name__, url_prefix='/instituicoes')


@instituicao_json_bp.get("/")
def get_all_instituicoes_json():
    service = InstituicaoEnsinoService()
    return jsonify(service.get_all_json()), 200


@instituicao_json_bp.get("/<int:id>")
def get_instituicao_by_id_json(id):
    service = InstituicaoEnsinoService()
    instituicao = service.get_by_id_json(id)
    if instituicao is None:
        return {"mensagem": "Instituição de ensino não encontrada"}, 404
    return jsonify(instituicao), 200


@instituicao_json_bp.post("/")
def post_instituicao_json():
    try:
        payload = request.get_json()
        if "co_entidade" in payload:
            payload["co_entidade"] = str(payload["co_entidade"])
        data = instituicaoEnsinoSchema.load(payload)
        service = InstituicaoEnsinoService()
        novo = service.create_json(data)
        return jsonify(novo), 201
    except ValidationError as err:
        return {"erro": "Dados inválidos", "campos": err.messages}, 400


@instituicao_json_bp.put("/<int:id>")
def put_instituicao_json(id):
    try:
        payload = request.get_json()
        if "co_entidade" in payload:
            payload["co_entidade"] = str(payload["co_entidade"])
        data = instituicaoEnsinoSchema.load(payload)
        service = InstituicaoEnsinoService()
        atualizado = service.update_json(id, data)
        if atualizado is None:
            return {"mensagem": "Instituição de ensino não encontrada"}, 404
        return jsonify(atualizado), 200
    except ValidationError as err:
        return {"erro": "Dados inválidos", "campos": err.messages}, 400


@instituicao_json_bp.delete("/<int:id>")
def delete_instituicao_json(id):
    service = InstituicaoEnsinoService()
    removido = service.delete_json(id)
    if not removido:
        return {"mensagem": "Instituição de ensino não encontrada"}, 404
    return {"mensagem": "Instituição de ensino removida com sucesso"}, 200
