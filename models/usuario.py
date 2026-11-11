from marshmallow import Schema, fields, validate


class Usuario:

    def __init__(self, nome, cpf, nascimento=None, email=None, id=None):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.nascimento = nascimento
        self.email = email

    def toDict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cpf": self.cpf,
            "nascimento": self.nascimento,
            "email": self.email
        }


class UsuarioSchema(Schema):

    id = fields.Int(dump_only=True)

    nome = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255)
    )

    cpf = fields.Str(
        required=True,
        validate=validate.Length(min=11, max=14)
    )

    nascimento = fields.Str(
        required=False,
        allow_none=True
    )

    email = fields.Str(
        required=False,
        allow_none=True
    )
