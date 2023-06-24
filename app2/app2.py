from flask import Flask
from controller.controller_app import index

# criação do app principal
app = Flask("competition controller 2", template_folder="view", static_folder="static")

app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

# registra controles
app.register_blueprint(index)

app.run()
