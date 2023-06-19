from Class.data_item_lock_manager import dataItemLockManager
from Class.transacao import transacao

data_items = ['q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
data_item_lock_manager = dataItemLockManager(data_items)
transacoes = transacao(data_items)

def create_new_transaction():
    transacoes.get_new_transaction(data_item_lock_manager.create_transaction_name())

def read_item(transaction_name, item):
    transacoes.data_items_of_transactions_list[int(transaction_name[-1]) - 1][item] = data_item_lock_manager.data_items[item]

def set_transaction_readed_item(transaction_name, item):
    transacoes.read_item(data_item_lock_manager.lock_register, transaction_name, item,
                         data_item_lock_manager.data_items)

def write_item(transaction_name, item_to_be_changed, item_one, item_two, value):
    query_one = check_if_data_item_is_updated_in_transaction(transaction_name, item_to_be_changed, item_one)
    query_two = check_if_data_item_is_updated_in_transaction(transaction_name, item_to_be_changed, item_two)
    if query_one == True and query_two == True:
        transacoes.data_items_of_transactions_list[int(transaction_name[-1]) - 1][item_to_be_changed] = value
        data_item_lock_manager.data_items[item_to_be_changed] = value
        print('Escrita de item feita no item ' + item_to_be_changed + 'para a ' + transaction_name + '!')

def check_if_data_item_is_updated_in_transaction(transaction_name, item_to_be_changed, item):
    if item.isnumeric() == False:
        if transacoes.data_items_of_transactions_list[int(transaction_name[-1]) - 1][item] == data_item_lock_manager.data_items[item]:
            return True
        else:
            print(item_to_be_changed + " não pode ser atualizado, para realizar essa ação, faça leitura do valor "
                                       "atualizado de " + item + " para a " + transaction_name + "!")


# def set_transaction_writed_item(item):
#     pass




#abaixo testes, acima código mesmo
# chaves = ["a", "b", "c"]
# meu_dicionario = {chave: 0 for chave in chaves}
#
# meu_dicionario['a'] = 1
# print(meu_dicionario)
#
# #
# print(meu_dicionario['a'])
#
# item_teste = 'c'
# print(lista)

#testes 3
# lista = []
#
# print(lista)
#
# if lista == []:
#     print('s')
#
# for i in lista:
#     print(i)
# # lista = []
#
# print(lista)
#
# if lista == []:
#     print('s')
#
# for i in lista:
#     print(i)