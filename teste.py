# lista = [['isso', [1]]]
#
# print(len(lista[0][1]))
#
#
#
# print(lista)
#
# conta = '1+2'
# print(type(eval(conta)))
#
# conta_two = 'A+30'
#
# conta_two = conta_two.replace('A','20')
#
# conta_two = eval(conta_two)
# print(conta_two)

# a = '12'
# b = 15
# c = 20
# d = 30
#
# print(isinstance(a,int))
#
# def aleatory(entrada, outraentrada, ultima):
#     print(entrada)
#
# aleatory('oi', None, None)

outputs = ['Primeira linha', 'Segunda linha']
output = ''

def find_output():
    outputs = ['Primeira linha', 'Segunda linha']
    output = ''
    for i in outputs:
        output = output + i + '\n'
    if len(outputs) == 1:
        return output

print(find_output())

if find_output() == None:
    print('hi')

isso = find_output()

print('isso'+str(isso))