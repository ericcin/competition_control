from flask import Flask
from controller.controller_app import index

# criação do app principal
app = Flask("competition controller", template_folder="view", static_folder="static")

# registra controles
app.register_blueprint(index)

app.run()
