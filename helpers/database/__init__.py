import psycopg2
from flask import g

from helpers.application import app
from helpers.enviroment import enviroment


def get_connection():
    conn = getattr(g, '_database', None)
    if conn is None or conn.closed:
        host = enviroment.get("DB_HOST", "localhost")
        port = int(enviroment.get("DB_PORT", 5435))
        dbname = enviroment.get("DB_NAME", "censoescolar")
        user = enviroment.get("DB_USER", "postgres")
        password = enviroment.get("DB_PASSWORD", "123456")

        conn = g._database = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
    return conn


@app.teardown_appcontext
def close_connection(exception):
    conn = getattr(g, '_database', None)
    if conn is not None and not conn.closed:
        conn.close()
