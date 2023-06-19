"""
Module Name: concurrency-main
Author: Equipe 3
Purpose: Inicializar um servidor Flask que recebe comandos para simular
            transações concorrentes em um BD.
Created: 2023-06-13
"""
import os
import secrets
from pathlib import Path

import flask

# Barra de debug
from flask_debugtoolbar import DebugToolbarExtension

from lock_manager_dispatching import init_lock_manager, lock_manager_dispatcher
from transaction_manager_dispatching import init_transaction_manager, transaction_manager_dispatcher
from settings import debug_message, info_message, init_logger

logger = init_logger(__name__)

app = flask.Flask(__name__)

# Inicializando a barra de debug
SECRET_FILE_PATH = Path(".flask_secret")
try:
    with SECRET_FILE_PATH.open("r") as secret_file:
        app.secret_key = secret_file.read()
except FileNotFoundError:
    # Let's create a cryptographically secure code in that file
    with SECRET_FILE_PATH.open("w") as secret_file:
        app.secret_key = secrets.token_hex(32)
        secret_file.write(app.secret_key)

app.debug = True
toolbar = DebugToolbarExtension(app)


@app.before_request
def preprocess_request() -> None:
    logger.debug(f"preprocess_request: request.method: {flask.request.method}")
    logger.debug(f"preprocess_request: request.headers: {flask.request.headers}")
    logger.debug(f"preprocess_request: request.path: {flask.request.path}")
    logger.debug(f"preprocess_request: request.cookies: {flask.request.cookies}")
    logger.debug(f"preprocess_request: request.get_data(): {flask.request.get_data()}")


@app.route("/")
def index():
    return flask.render_template("index.html")


#  flask.send_file(
#                       path_or_file,
#                       mimetype=None,
#                       as_attachment=False,
#                       download_name=None,
#                       conditional=True,
#                       etag=True,
#                       last_modified=None,
#                       max_age=None)
@app.route("/favicon.ico")
def favicon():
    debug_message("favicon: " + os.getcwd())
    return flask.send_file(
        "favicon.ico",
        mimetype="image/x-icon",
        download_name="favicon.ico",
    )


# Rota para o gerenciador de bloqueios
@app.route("/LockManager", methods=["GET", "POST"])
def lock_manager():
    info_message("/LockManager reached.")

    try:
        data = flask.request.get_json()
        info_message(f"lock_manager: data: {data}")
        method = data.get("method")
        message = data.get("message")
        result = lock_manager_dispatcher(method, message)
    except Exception as e:
        error_message = f"lock_manager: {str(e)}"
        result = {"error": error_message}
    info_message(f"lock_manager: result: {result}")
    result_jsonified = flask.jsonify(result)
    info_message(f"lock_manager: result_jsonified: {result_jsonified}")
    return result_jsonified

# Rota para o gerenciador de transações
@app.route("/TransactionManager", methods=["GET", "POST"])
def transaction_manager():
    info_message("/TransactionManager reached.")

    try:
        data = flask.request.get_json()
        info_message(f"transaction_manager: data: {data}")
        method = data.get("method")
        message = data.get("message")
        result = transaction_manager_dispatcher(method, message)
    except Exception as e:
        error_message = f"transaction_manager: {str(e)}"
        result = {"error": error_message}
    info_message(f"transaction_manager: result: {result}")
    result_jsonified = flask.jsonify(result)
    info_message(f"transaction_manager: result_jsonified: {result_jsonified}")
    return result_jsonified


def main() -> None:
    info_message(f"main: Flask version: {flask.__version__}")
    app.run()


if __name__ == "__main__":
    main()
