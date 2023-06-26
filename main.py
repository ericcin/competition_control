from Class.data_item_lock_manager import dataItemLockManager
from Class.transacao import transacao

data_items = ['q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
data_item_lock_manager = dataItemLockManager(data_items)
transacoes = transacao(data_items)


def create_new_transaction():
    transaction_name = data_item_lock_manager.create_transaction_name()
    transacoes.get_new_transaction(transaction_name)
    return transaction_name


def write_lock(data_item, transaction):
    return data_item_lock_manager.write_lock(data_item, transaction)


def read_lock(data_item, transaction):
    return data_item_lock_manager.read_lock(data_item, transaction)


def unlock(data_item, transaction):
    return data_item_lock_manager.unlock(data_item, transaction)


def read_item(transaction_name, item):
    if data_item_lock_manager.can_read_item(transaction_name, item):
        transacoes.read_item(transaction_name, item, data_item_lock_manager.data_items)
        data_item_lock_manager.insert_in_complete_lock_register(item, 'read_item', 1, transaction_name)
        return 'Leitura de item realizada no item ' + item + ' para a ' + transaction_name + '!'
    else:
        data_item_lock_manager.get_error()
        return ('Leitura de item não realizada, pois a ' + transaction_name + ' não possui bloqueio sobre o item ' +
                item + '!')

def write_item(transaction_name, item_to_be_changed, item_one, item_two, arithmetic_sign):
    if not check_if_a_item_in_write_item_is_numeric(item_one) and not check_if_a_item_in_write_item_is_numeric(item_two):
        value = write_item_with_two_non_numeric_items(transaction_name, item_to_be_changed, item_one, item_two,
                                                     arithmetic_sign)

    if not check_if_a_item_in_write_item_is_numeric(item_one) and check_if_a_item_in_write_item_is_numeric(
        item_two) or check_if_a_item_in_write_item_is_numeric(item_one) and not check_if_a_item_in_write_item_is_numeric(
        item_two):
        value = write_item_with_one_numeric_item(transaction_name, item_to_be_changed, item_one, item_two,
                                                     arithmetic_sign)

    if check_if_a_item_in_write_item_is_numeric(item_one) and check_if_a_item_in_write_item_is_numeric(item_two):
        value = write_item_with_two_numeric_itens(transaction_name, item_to_be_changed, item_one, item_two,
                                                     arithmetic_sign)

    if isinstance(value, int):
        if data_item_lock_manager.write_item(transaction_name, item_to_be_changed, value):
            transacoes.write_item(transaction_name, item_to_be_changed, value)
            return 'Escrita de item feita no item ' + item_to_be_changed + 'para a ' + transaction_name + '!'
        else:
            return 'Escrita de item não realizada, pois a ' + transaction_name + \
                ' não possui bloqueio exclusivo sobre o item ' + item_to_be_changed + '!'

def write_item_with_two_non_numeric_items(transaction_name, item_to_be_changed, item_one, item_two, arithmetic_sign):
    query_one = check_if_data_item_is_updated_in_transaction(transaction_name, item_to_be_changed, item_one)
    if not query_one:
        return (item_to_be_changed + " não pode ser atualizado, para realizar essa ação, faça leitura do valor "
                                     "atualizado de " + item_one + " para a " + transaction_name + "!")
    query_two = check_if_data_item_is_updated_in_transaction(transaction_name, item_to_be_changed, item_two)
    if not query_two:
        return (item_to_be_changed + " não pode ser atualizado, para realizar essa ação, faça leitura do valor "
                                     "atualizado de " + item_two + " para a " + transaction_name + "!")
    if query_one and query_two:
        query_three = check_if_non_numeric_item_have_1_length(item_one)
        if query_three:
            item_one = str(data_item_lock_manager[item_one])
        else:
            return ('Erro crítico! O item um: ' + item_one + ' possui mais de 1 carácter. Refaça a operação levando'
                                                             'em conta itens de dados com apenas um caractere')

        query_four = check_if_non_numeric_item_have_1_length(item_two)
        if query_four:
            item_two = str(data_item_lock_manager[item_two])
        else:
            return ('Erro crítico! O item um: ' + item_two + ' possui mais de 1 carácter. Refaça a operação levando'
                                                             'em conta itens de dados com apenas um caractere')
        if query_three and query_four:
            value = item_one + arithmetic_sign + item_two
            value = eval(value)
            return value

def write_item_with_one_numeric_item(transaction_name, item_to_be_changed, item_one, item_two, arithmetic_sign):
    if not check_if_a_item_in_write_item_is_numeric(item_one):
        query_one = check_if_data_item_is_updated_in_transaction(transaction_name, item_to_be_changed, item_one)
        if not query_one:
            return (item_to_be_changed + " não pode ser atualizado, para realizar essa ação, faça leitura do valor "
                                         "atualizado de " + item_one + " para a " + transaction_name + "!")
        else:
            query_three = check_if_non_numeric_item_have_1_length(item_one)
            if query_three:
                item_one = str(data_item_lock_manager[item_one])
                value = item_one + arithmetic_sign + item_two
                value = eval(value)
                return value
            else:
                return ('Erro crítico! O item um: ' + item_one + ' possui mais de 1 carácter. Refaça a operação levando'
                                                                 'em conta itens de dados com apenas um caractere')

    if not check_if_a_item_in_write_item_is_numeric(item_two):
        query_two = check_if_data_item_is_updated_in_transaction(transaction_name, item_to_be_changed, item_two)
        if not query_two:
            return (item_to_be_changed + " não pode ser atualizado, para realizar essa ação, faça leitura do valor "
                                         "atualizado de " + item_two + " para a " + transaction_name + "!")
        else:
            query_four = check_if_non_numeric_item_have_1_length(item_two)
            if query_four:
                item_two = str(data_item_lock_manager[item_two])
                value = item_one + arithmetic_sign + item_two
                value = eval(value)
                return value
            else:
                return ('Erro crítico! O item dois: ' + item_two + ' possui mais de 1 carácter. Refaça a operação levando'
                                                                 'em conta itens de dados com apenas um caractere')
def write_item_with_two_numeric_itens(transaction_name, item_to_be_changed, item_one, item_two, arithmetic_sign):
    value = item_one + arithmetic_sign + item_two
    value = eval(value)
    return value

def solve_errors():
    solve_lock_errors()
    solve_write_and_read_item_errors()

def  solve_lock_errors():
    data_item_lock_manager.solve_error()

def solve_write_and_read_item_errors():
    #[data_item, transaction, attempted_action, cause, item_one_in_write_item, item_two_in_write_item]
    if data_item_lock_manager.errors != []:
        for i in data_item_lock_manager.errors:
            if i[2] == 'read_item':
                read_lock(i[0], i[1])
                read_item(i[1], i[0])
            if i[2] == 'write_item':
                if i[3] == 'item_one':
                    if i[0] == i[4]:
                        write_lock(i[0], i[1])
                        read_item(i[1], i[0])
                        write_item(i[1], i[0], i[4], i[5])
                    else:
                        read_lock(i[0], i[1])
                        read_item(i[1], i[0])
                        write_item(i[1], i[0], i[4], i[5])
                if i[3] == 'item_two':
                    if i[0] == i[4]:
                        write_lock(i[0], i[1])
                        read_item(i[1], i[0])
                        write_item(i[1], i[0], i[4], i[5])
                    else:
                        read_lock(i[0], i[1])
                        read_item(i[1], i[0])
                        write_item(i[1], i[0], i[4], i[5])

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