from Class.data_item_lock_manager import dataItemLockManager
from Class.transacao import transacao

data_items = ['q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
data_item_lock_manager = dataItemLockManager(data_items)
transacoes = transacao(data_items)

def create_new_transaction():
    transacoes.get_new_transaction(data_item_lock_manager.create_transaction_name())

def set_transaction_readed_item(transaction_name, item):
    transacoes.read_item(data_item_lock_manager.lock_register, transaction_name, item,
                         data_item_lock_manager.data_items)

def write_item(transaction_name, item):
    pass

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