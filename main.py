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
        return ('Leitura de item não realizada, pois a ' + transaction_name + ' não possui bloqueio sobre o item ' +
                item + '!')


def write_item(transaction_name, item_to_be_changed, item_one, item_two, value):
    query_one = check_if_data_item_is_updated_in_transaction(transaction_name, item_to_be_changed, item_one)
    if not query_one:
        return (item_to_be_changed + " não pode ser atualizado, para realizar essa ação, faça leitura do valor "
                                     "atualizado de " + item_one + " para a " + transaction_name + "!")
    query_two = check_if_data_item_is_updated_in_transaction(transaction_name, item_to_be_changed, item_two)
    if not query_two:
        return (item_to_be_changed + " não pode ser atualizado, para realizar essa ação, faça leitura do valor "
                                     "atualizado de " + item_two + " para a " + transaction_name + "!")
    if query_one and query_two:
        if data_item_lock_manager.write_item(transaction_name, item_to_be_changed, value):
            transacoes.write_item(transaction_name, item_to_be_changed, value)
            return 'Escrita de item feita no item ' + item_to_be_changed + 'para a ' + transaction_name + '!'
        else:
            return 'Escrita de item não realizada, pois a ' + transaction_name + \
                   ' não possui bloqueio exclusivo sobre o item ' + item_to_be_changed + '!'


def check_if_data_item_is_updated_in_transaction(transaction_name, item_to_be_changed, item):
    if not item.isnumeric():
        if transacoes.data_items_of_transactions_list[int(transaction_name[-1]) - 1][item] == \
                data_item_lock_manager.data_items[item]:
            return True
        else:
            return False
    else:
        return True  # remover posteriormente
