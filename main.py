chaves = ["a", "b", "c"]
meu_dicionario = {chave: 0 for chave in chaves}

meu_dicionario['a'] = 1
print(meu_dicionario)

print(meu_dicionario['a'])

item_teste = 'c'

if item_teste not in meu_dicionario:
    print(item_teste+' nao esta no dicionario')

# lista = ['x', 'read_lock', 1, ['transacao1']]
#
# lista[3].append('transacao2')
#
# print(str(lista[3])+'essas')