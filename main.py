from Class.data_item_lock_manager import dataItemLockManager
from Class.transacao import transacao

data_items = ['q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
data_item_lock_manager = dataItemLockManager(data_items)
transacoes = transacao(data_items)


def get_locks():
    return data_item_lock_manager.get_locks()


def get_complete_locks():
    return data_item_lock_manager.get_complete_locks()


def create_new_transaction():
    transaction_name = data_item_lock_manager.create_transaction_name()
    transacoes.get_new_transaction(transaction_name)
    return transaction_name


def write_lock(data_item, transaction):
    if transaction not in transacoes.get_shrinking():
        return data_item_lock_manager.write_lock(data_item, transaction)
    else:
        return {'text': 'Transação ' + transaction + ' em fase de encolhimento, não é possivel realizar bloqueios',
                'value': False}


def read_lock(data_item, transaction):
    if transaction not in transacoes.get_shrinking():
        return data_item_lock_manager.read_lock(data_item, transaction)
    else:
        return {'text': 'Transação ' + transaction + ' em fase de encolhimento, não é possivel realizar bloqueios',
                'value': False}


def unlock(data_item, transaction):
    output = data_item_lock_manager.unlock(data_item, transaction)
    if output['value']:
        transacoes.add_shrinking(transaction)
    return output


def read_item(transaction_name, item):
    if transaction_name not in transacoes.get_shrinking():
        if data_item_lock_manager.can_read_item(transaction_name, item):
            transacoes.read_item(transaction_name, item, data_item_lock_manager.data_items)
            data_item_lock_manager.insert_in_complete_lock_register(item, 'read_item', 1, transaction_name)
            return {'text': 'Leitura de item realizada no item ' + item + ' para a ' + transaction_name + '!',
                    'value': True}
        else:
            data_item_lock_manager.get_error(item, transaction_name, 'read_item', 'write_lock', None, None)
            return {
                'text': 'Leitura de item não realizada, pois a ' + transaction_name + ' não possui bloqueio sobre o item ' +
                        item + '!', 'value': False}
    else:
        return {'text': 'Transação ' + transaction_name + ' em fase de encolhimento, não é possivel realizar alterações',
                'value': False}


def write_item(transaction_name, item_to_be_changed, item_one, item_two, arithmetic_sign):
    if transaction_name not in transacoes.get_shrinking():
        if not check_if_a_item_in_write_item_is_numeric(item_one) and not check_if_a_item_in_write_item_is_numeric(
                item_two):
            value = write_item_with_two_non_numeric_items(transaction_name, item_to_be_changed, item_one, item_two,
                                                          arithmetic_sign)

        if not check_if_a_item_in_write_item_is_numeric(item_one) and check_if_a_item_in_write_item_is_numeric(
                item_two) or check_if_a_item_in_write_item_is_numeric(
            item_one) and not check_if_a_item_in_write_item_is_numeric(
            item_two):
            value = write_item_with_one_numeric_item(transaction_name, item_to_be_changed, item_one, item_two,
                                                     arithmetic_sign)

        if check_if_a_item_in_write_item_is_numeric(item_one) and check_if_a_item_in_write_item_is_numeric(item_two):
            value = write_item_with_two_numeric_itens(transaction_name, item_to_be_changed, item_one, item_two,
                                                      arithmetic_sign)

        if isinstance(value, int):
            if data_item_lock_manager.write_item(transaction_name, item_to_be_changed, value):
                transacoes.write_item(transaction_name, item_to_be_changed, value)
                return {'text': 'Escrita de item feita no item ' + item_to_be_changed + 'para a ' + transaction_name + '!',
                        'value': True}
            else:
                data_item_lock_manager.get_error(item_to_be_changed, transaction_name, 'write_item', 'write_lock', item_one,
                                                 item_two)
                return {'text': 'Escrita de item não realizada, pois a ' + transaction_name + \
                                ' não possui bloqueio exclusivo sobre o item ' + item_to_be_changed + '!', 'value': False}
        else:
            return value
    else:
        return {'text': 'Transação ' + transaction_name + ' em fase de encolhimento, não é possivel realizar alterações',
                'value': False}


def write_item_with_two_non_numeric_items(transaction_name, item_to_be_changed, item_one, item_two, arithmetic_sign):
    query_one = check_if_data_item_is_updated_in_transaction(transaction_name, item_to_be_changed, item_one)
    if not query_one:
        data_item_lock_manager.get_error(item_to_be_changed, transaction_name, 'write_item', 'item_one', item_one,
                                         item_two)
        return {'text': item_to_be_changed + " não pode ser atualizado, para realizar essa ação, faça leitura do valor "
                                             "atualizado de " + item_one + " para a " + transaction_name + "!",
                'value': False}
    query_two = check_if_data_item_is_updated_in_transaction(transaction_name, item_to_be_changed, item_two)
    if not query_two:
        data_item_lock_manager.get_error(item_to_be_changed, transaction_name, 'write_item', 'item_two', item_one,
                                         item_two)
        return {'text': item_to_be_changed + " não pode ser atualizado, para realizar essa ação, faça leitura do valor "
                                             "atualizado de " + item_two + " para a " + transaction_name + "!",
                'value': False}
    if query_one and query_two:
        query_three = check_if_non_numeric_item_have_1_length(item_one)
        if query_three:
            item_one = str(data_item_lock_manager.data_items[item_one])
        else:
            return {
                'text': 'Erro crítico! O item um: ' + item_one + ' possui mais de 1 carácter. Refaça a operação '
                                                                 'levando em conta itens de dados com apenas um caractere',
                'value': False}

        query_four = check_if_non_numeric_item_have_1_length(item_two)
        if query_four:
            item_two = str(data_item_lock_manager.data_items[item_two])
        else:
            return {
                'text': 'Erro crítico! O item um: ' + item_two + ' possui mais de 1 carácter. Refaça a operação levando'
                                                                 'em conta itens de dados com apenas um caractere',
                'value': False}
        if query_three and query_four:
            value = item_one + arithmetic_sign + item_two
            value = eval(value)
            return value


def write_item_with_one_numeric_item(transaction_name, item_to_be_changed, item_one, item_two, arithmetic_sign):
    if not check_if_a_item_in_write_item_is_numeric(item_one):
        query_one = check_if_data_item_is_updated_in_transaction(transaction_name, item_to_be_changed, item_one)
        if not query_one:
            data_item_lock_manager.get_error(item_to_be_changed, transaction_name, 'write_item', 'item_one', item_one,
                                             item_two)
            return {
                'text': item_to_be_changed + " não pode ser atualizado, para realizar essa ação, faça leitura do valor "
                                             "atualizado de " + item_one + " para a " + transaction_name + "!",
                'value': False}
        else:
            query_three = check_if_non_numeric_item_have_1_length(item_one)
            if query_three:
                item_one = str(data_item_lock_manager.data_items[item_one])
                value = item_one + arithmetic_sign + item_two
                value = eval(value)
                return value
            else:
                return {
                    'text': 'Erro crítico! O item um: ' + item_one + ' possui mais de 1 carácter. '
                                                                     'Refaça a operação levando ' 'em conta itens de dados com apenas um caractere',
                    'value': False}

    if not check_if_a_item_in_write_item_is_numeric(item_two):
        query_two = check_if_data_item_is_updated_in_transaction(transaction_name, item_to_be_changed, item_two)
        if not query_two:
            data_item_lock_manager.get_error(item_to_be_changed, transaction_name, 'write_item', 'item_two', item_one,
                                             item_two)
            return {
                'text': item_to_be_changed + " não pode ser atualizado, para realizar essa ação, faça leitura do valor "
                                             "atualizado de " + item_two + " para a " + transaction_name + "!",
                'value': False}
        else:
            query_four = check_if_non_numeric_item_have_1_length(item_two)
            if query_four:
                item_two = str(data_item_lock_manager.data_items[item_two])
                value = item_one + arithmetic_sign + item_two
                value = eval(value)
                return value
            else:
                return {
                    'text': 'Erro crítico! O item dois: ' + item_two + 'possui mais de 1 carácter. '
                                                                       'Refaça a operação levando em conta itens de dados com apenas um caractere',
                    'value': False}


def write_item_with_two_numeric_itens(transaction_name, item_to_be_changed, item_one, item_two, arithmetic_sign):
    value = item_one + arithmetic_sign + item_two
    value = eval(value)
    return value


def solve_errors():
    output_one = solve_lock_errors()
    output_two = solve_write_and_read_item_errors()

    if output_one != None:
        return output_one

    if output_two != None:
        return output_two


def solve_lock_errors():
    output_one = data_item_lock_manager.solve_error()
    return output_one


def solve_write_and_read_item_errors():
    # [data_item, transaction, attempted_action, cause, item_one_in_write_item, item_two_in_write_item]
    outputs = []
    if data_item_lock_manager.errors != []:
        for i in data_item_lock_manager.errors:
            if i[2] == 'read_item':
                outputs.append(read_lock(i[0], i[1]))
                outputs.append(read_item(i[1], i[0]))
            if i[2] == 'write_item':
                if i[3] == 'item_one':
                    if i[0] == i[4]:
                        outputs.append(write_lock(i[0], i[1]))
                        outputs.append(read_item(i[1], i[0]))
                        outputs.append(write_item(i[1], i[0], i[4], i[5]))
                    else:
                        outputs.append(read_lock(i[0], i[1]))
                        outputs.append(read_item(i[1], i[0]))
                        outputs.append(write_item(i[1], i[0], i[4], i[5]))
                if i[3] == 'item_two':
                    if i[0] == i[4]:
                        outputs.append(write_lock(i[0], i[1]))
                        outputs.append(read_item(i[1], i[0]))
                        outputs.append(write_item(i[1], i[0], i[4], i[5]))
                    else:
                        outputs.append(read_lock(i[0], i[1]))
                        outputs.append(read_item(i[1], i[0]))
                        outputs.append(write_item(i[1], i[0], i[4], i[5]))
                if i[3] == 'read_lock':
                    data_item_lock_manager.has_shared_lock(i[0])
                    for j in data_item_lock_manager.lock_register[data_item_lock_manager.array_position][3]:
                        outputs.append(data_item_lock_manager.unlock(i[0], j))
                    write_lock(i[0], i[1])

    if outputs != []:
        output = ''
        for i in outputs:
            output = output + str(i) + '\n'
        return {'text': output, 'value': True}


def check_if_data_item_is_updated_in_transaction(transaction_name, item_to_be_changed, item):
    if transacoes.data_items_of_transactions_list[int(transaction_name[-1]) - 1][item] == \
            data_item_lock_manager.data_items[item]:
        return True
    else:
        return False


def check_if_a_item_in_write_item_is_numeric(item):
    return item.isnumeric()


def check_if_non_numeric_item_have_1_length(item):
    if not item.isdigit():
        if len(item) == 1:
            return True
        else:
            return False
