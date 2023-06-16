# chaves = ["a", "b", "c"]
# meu_dicionario = {chave: 0 for chave in chaves}
#
# meu_dicionario['a'] = 1
# print(meu_dicionario)
#
# print(meu_dicionario['a'])
#
# item_teste = 'c'
#
# if item_teste not in meu_dicionario:
#     print(item_teste+' nao esta no dicionario')

#testes2
# lista = [['x', 'read_lock', 1, ['transacao1']]]
#
# lista[0][3].append('transacao2')
#
# print(str(lista[0])+'essas')
#
# lista.append(['z', 'write_lock', 1, ['transacao3']])
#
# if 'transacao2' in lista[0][3]:
#     print('OK')
#
# for i in lista:
#     print(i)
#     if 'x' in i and 'read_lock' in i:
#         print('X ESTA NA LISTA')
# #
# # if'x' in lista:
# #     print('X EM LISTA')
# print("LISTA ANTES DO DEL")
# print(lista)
# del lista[0]
# print("DEL FEITO")
# print(lista)

#testes 3
lista = []

print(lista)

if lista == []:
    print('s')

for i in lista:
    print(i)