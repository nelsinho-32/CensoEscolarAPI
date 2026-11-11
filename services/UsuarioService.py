from repositories.UsuarioRepository import UsuarioRepository


class UsuarioService():
    def __init__(self):
        self.usuarioRepository = UsuarioRepository()

    def get_all(self):
        return self.usuarioRepository.getUsuarios()

    def get_by_id(self, id):
        return self.usuarioRepository.getUsuario(id)

    def create(self, data):
        return self.usuarioRepository.createUsuario(data)

    def update(self, id, data):
        return self.usuarioRepository.updateUsuario(id, data)

    def delete(self, id):
        return self.usuarioRepository.deleteUsuario(id)
