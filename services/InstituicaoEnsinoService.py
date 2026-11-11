from helpers.logger import logger
from repositories.InstituicaoEnsinoRepository import InstituicaoEnsinoRepository


class InstituicaoEnsinoService():
    def __init__(self):
        self.instituicaoEnsinoRepository = InstituicaoEnsinoRepository()

    def get_all(self, page=1, limit=100):
        logger.info("Recuperando a lista de instituições no banco de dados")
        return self.instituicaoEnsinoRepository.getInstituicoes(page, limit)

    def get_by_id(self, id):
        return self.instituicaoEnsinoRepository.getInstituicao(id)

    def create(self, data):
        return self.instituicaoEnsinoRepository.createInstituicao(data)

    def update(self, id, data):
        return self.instituicaoEnsinoRepository.updateInstituicao(id, data)

    def delete(self, id):
        return self.instituicaoEnsinoRepository.deleteInstituicao(id)

    def get_all_json(self):
        return self.instituicaoEnsinoRepository.getInstituicoesJson()

    def get_by_id_json(self, id):
        return self.instituicaoEnsinoRepository.getInstituicaoJson(id)

    def create_json(self, data):
        return self.instituicaoEnsinoRepository.createInstituicaoJson(data)

    def update_json(self, id, data):
        return self.instituicaoEnsinoRepository.updateInstituicaoJson(id, data)

    def delete_json(self, id):
        return self.instituicaoEnsinoRepository.deleteInstituicaoJson(id)
