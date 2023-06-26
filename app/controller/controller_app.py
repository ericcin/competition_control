from flask import Blueprint, render_template, request, json
import main

index = Blueprint("index", "competition controller", template_folder="view", static_folder="static")


@index.route("/")
def homepage():
    template = render_template("index.html")
    return template


@index.route("/get_itens/")
def get_itens():
    return main.data_items


# @index.route("/get_transaction/")
# def get_transaction():
#     return main.transacao.get_transactions_names()


@index.route("/new_transaction/", methods=['POST'])
def new_transaction():
    transaction_name = main.create_new_transaction()
    return json.dumps({'status': 'OK', 'result': transaction_name})


@index.route("/action/", methods=['POST'])
def realizar_acao():
    transaction = request.form['transaction']
    action = request.form['action']
    item = request.form['item']
    value1 = request.form['value1']
    operator = request.form['operator']
    value2 = request.form['value2']

    if action == "read_lock":
        result = main.read_lock(item, transaction)
    elif action == "read_item":
        result = main.read_item(transaction, item)
    elif action == "write_lock":
        result = main.write_lock(item, transaction)
    elif action == "write_item":
        result = main.write_item(transaction, item, value1, value2, operator)
    elif action == "unlock":
        result = main.unlock(item, transaction)
    else:
        return json.dumps({'status': '400'})

    return json.dumps({'status': 'OK', 'result': result})
