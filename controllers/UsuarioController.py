from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from models.usuario import UsuarioSchema
from services.UsuarioService import UsuarioService
from helpers.logger import logger

usuarioSchema = UsuarioSchema()
usuariosSchema = UsuarioSchema(many=True)

usuario_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')


@usuario_bp.get("/")
def get_all_usuarios():
    logger.info("Listando usuários")
    service = UsuarioService()
    usuarios = service.get_all()
    return jsonify(usuariosSchema.dump(usuarios)), 200


@usuario_bp.get("/<int:id>")
def get_usuario_by_id(id):
    service = UsuarioService()
    usuario = service.get_by_id(id)
    if usuario is None:
        return {"mensagem": "Usuário não encontrado"}, 404
    return jsonify(usuarioSchema.dump(usuario)), 200


@usuario_bp.post("/")
def post_usuario():
    try:
        data = usuarioSchema.load(request.get_json())
        service = UsuarioService()
        usuario = service.create(data)
        return jsonify(usuarioSchema.dump(usuario)), 201
    except ValidationError as err:
        return {"erro": "Dados inválidos", "campos": err.messages}, 400


@usuario_bp.put("/<int:id>")
def put_usuario(id):
    try:
        data = usuarioSchema.load(request.get_json())
        service = UsuarioService()
        usuario = service.update(id, data)
        if usuario is None:
            return {"mensagem": "Usuário não encontrado"}, 404
        return jsonify(usuarioSchema.dump(usuario)), 200
    except ValidationError as err:
        return {"erro": "Dados inválidos", "campos": err.messages}, 400


@usuario_bp.delete("/<int:id>")
def delete_usuario(id):
    service = UsuarioService()
    removido = service.delete(id)
    if not removido:
        return {"mensagem": "Usuário não encontrado"}, 404
    return {"mensagem": "Usuário removido com sucesso"}, 200
