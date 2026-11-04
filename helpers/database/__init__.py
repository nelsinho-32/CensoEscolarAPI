import sqlite3
from flask import g

from helpers.application import app
from helpers.enviroment import enviroment

DATABASE = enviroment.get("DB_NAME")


def get_connection():
    conn = getattr(g, '_database', None)
    if conn is None:
        conn = g._database = sqlite3.connect(DATABASE)
    return conn


@app.teardown_appcontext
def close_connection(exception):
    conn = getattr(g, '_database', None)
    if conn is not None:
        conn.close()
