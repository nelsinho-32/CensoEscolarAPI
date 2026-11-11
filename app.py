from helpers.application import app
from helpers.enviroment import enviroment
from controllers.IntituicaoEnsinoController import instituicao_ensino_bp
from controllers.InstituicaoJsonController import instituicao_json_bp
from controllers.UsuarioController import usuario_bp
from controllers.IndexController import index_bp

app.register_blueprint(instituicao_ensino_bp)
app.register_blueprint(instituicao_json_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(index_bp)


def main(arg=[]):
    host = enviroment.get("DB_HOST", "127.0.0.1")
    port = int(enviroment.get("DB_PORT", 5000))
    app.run(host=host, port=port, debug=True)


if __name__ == '__main__':
    main()
