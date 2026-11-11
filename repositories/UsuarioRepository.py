from helpers.file.json import read, write
from models.usuario import Usuario

ARQUIVO_USUARIOS = "usuarios.json"


class UsuarioRepository():

    def getUsuarios(self):
        dataset = read(ARQUIVO_USUARIOS)
        return [
            Usuario(
                id=row.get("id"),
                nome=row.get("nome"),
                cpf=row.get("cpf"),
                nascimento=row.get("nascimento"),
                email=row.get("email")
            )
            for row in dataset
        ]

    def getUsuario(self, id):
        dataset = read(ARQUIVO_USUARIOS)
        for row in dataset:
            if int(row.get("id")) == int(id):
                return Usuario(
                    id=row.get("id"),
                    nome=row.get("nome"),
                    cpf=row.get("cpf"),
                    nascimento=row.get("nascimento"),
                    email=row.get("email")
                )
        return None

    def createUsuario(self, data):
        dataset = read(ARQUIVO_USUARIOS)
        novo_id = 1
        if len(dataset) > 0:
            novo_id = max(int(item["id"]) for item in dataset) + 1

        usuario = Usuario(
            id=novo_id,
            nome=data.get("nome"),
            cpf=data.get("cpf"),
            nascimento=data.get("nascimento"),
            email=data.get("email")
        )
        dataset.append(usuario.toDict())
        write(ARQUIVO_USUARIOS, dataset)
        return usuario

    def updateUsuario(self, id, data):
        dataset = read(ARQUIVO_USUARIOS)
        for i, row in enumerate(dataset):
            if int(row.get("id")) == int(id):
                usuario = Usuario(
                    id=int(id),
                    nome=data.get("nome"),
                    cpf=data.get("cpf"),
                    nascimento=data.get("nascimento"),
                    email=data.get("email")
                )
                dataset[i] = usuario.toDict()
                write(ARQUIVO_USUARIOS, dataset)
                return usuario
        return None

    def deleteUsuario(self, id):
        dataset = read(ARQUIVO_USUARIOS)
        for i, row in enumerate(dataset):
            if int(row.get("id")) == int(id):
                dataset.pop(i)
                write(ARQUIVO_USUARIOS, dataset)
                return True
        return False
