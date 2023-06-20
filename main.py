from Class.data_item_lock_manager import dataItemLockManager
from Class.transacao import transacao

data_items = ['q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
data_item_lock_manager = dataItemLockManager(data_items)
transacoes = transacao(data_items)

def create_new_transaction():
    transacoes.get_new_transaction(data_item_lock_manager.create_transaction_name())

def write_lock(data_item, transaction):
    data_item_lock_manager.write_lock(data_item, transaction)

def read_lock(data_item, transaction):
    data_item_lock_manager.read_lock(data_item, transaction)

def unlock(data_item, transaction):
    data_item_lock_manager.unlock(data_item, transaction)

def read_item(transaction_name, item):
    if data_item_lock_manager.can_read_item(transaction_name, item) == True:
        transacoes.read_item(transaction_name, item, data_item_lock_manager.data_items)
        return 'Leitura de item realizada no item ' + item + ' para a ' + transaction_name + '!'
    else:
        return ('Leitura de item não realizada, pois a ' + transaction_name + ' não possui bloqueio sobre o item ' +
                 item + '!')

def write_item(transaction_name, item_to_be_changed, item_one, item_two, value):
    query_one = check_if_data_item_is_updated_in_transaction(transaction_name, item_to_be_changed, item_one)
    if query_one == False:
        return(item_to_be_changed + " não pode ser atualizado, para realizar essa ação, faça leitura do valor "
                                   "atualizado de " + item_one + " para a " + transaction_name + "!")
    query_two = check_if_data_item_is_updated_in_transaction(transaction_name, item_to_be_changed, item_two)
    if query_two == False:
        print(item_to_be_changed + " não pode ser atualizado, para realizar essa ação, faça leitura do valor "
                                   "atualizado de " + item_two + " para a " + transaction_name + "!")
    if query_one == True and query_two == True:
        data_item_lock_manager.write_item(transaction_name, item_to_be_changed, value)
        if data_item_lock_manager.write_item_ok == True:
            transacoes.write_item(transaction_name, item_to_be_changed, value)
            data_item_lock_manager.write_item_ok = False
            return('Escrita de item feita no item ' + item_to_be_changed + 'para a ' + transaction_name + '!')

def check_if_data_item_is_updated_in_transaction(transaction_name, item_to_be_changed, item):
    if item.isnumeric() == False:
        if transacoes.data_items_of_transactions_list[int(transaction_name[-1]) - 1][item] == data_item_lock_manager.data_items[item]:
            return True
        else:
            return False