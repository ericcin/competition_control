from flask import Blueprint, render_template, request, json
from Class import data_item_lock_manager
from Class.data_item_lock_manager import dataItemLockManager

index = Blueprint("index", "competition controller", template_folder="view", static_folder="static")

data = dataItemLockManager(["x", "y", "z"])


@index.route("/")
def homepage():
    template = render_template("index.html")
    return template


@index.route("/action/", methods=['POST'])
def realizar_acao():
    transaction = request.form['transaction']
    action = request.form['action']
    item = request.form['item']
    value1 = request.form['value1']
    operator = request.form['operator']
    value2 = request.form['value2']

    if action == "read_lock":
        result = data.read_lock(item, transaction)
    elif action == "read_item":
        result = data.read_item(transaction, item, "0")
    elif action == "write_lock":
        result = data.write_lock(item, transaction)
    elif action == "write_item":
        result = data.write_item(transaction, item, "0")
    elif action == "unlock":
        result = data.unlock(item, transaction)
    else:
        return json.dumps({'status': '400'})

    return json.dumps({'status': 'OK', 'result': result})
