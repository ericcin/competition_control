from flask import Blueprint, render_template

index = Blueprint("index", "competition controller", template_folder="view", static_folder="static")


@index.route("/")
def homepage():
    template = render_template("index.html")
    return template
