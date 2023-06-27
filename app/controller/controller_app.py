from flask import Blueprint, render_template, request, json
import main

index = Blueprint("index", "competition controller", template_folder="view", static_folder="static")
fase = True


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
    global fase

    if action == "read_lock" and fase:
        result = main.read_lock(item, transaction)
    elif action == "read_item" and fase:
        result = main.read_item(transaction, item)
    elif action == "write_lock" and fase:
        result = main.write_lock(item, transaction)
    elif action == "write_item" and fase:
        result = main.write_item(transaction, item, value1, value2, operator)
    elif action == "unlock":
        result = main.unlock(item, transaction)
        fase = False
    else:
        result = {'text': 'Fase de encolhimento, somente é possivel liberar bloqueios!', 'value': False}
        return json.dumps({'status': 'Ok', 'result': result})

    return json.dumps({'status': 'OK', 'result': result})


@index.route("/solve_errors/", methods=['POST'])
def solve_errors():
    main.solve_errors()
    return json.dumps({'status': 'OK'})


@index.route("/get_locks/", methods=['POST'])
def get_locks():
    return main.get_locks()


@index.route("/get_complete_locks/", methods=['POST'])
def get_complete_locks():
    return main.get_complete_locks()
