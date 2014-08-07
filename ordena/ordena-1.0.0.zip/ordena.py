__author__ = 'Hunter'

def selecao(lista):
    n = len(lista)
    for i in range(n - 1):
        menor = i
        for j in range(i + 1, n):
            if lista[j] < lista[menor]:
                menor = j
            lista[i], lista[menor] = lista[menor], lista[i]
    return lista


def bolha(lista):
    for j in range(len(lista) - 1):
        for i in range(len(lista) - 1 - j):
            if lista[i] > lista[i + 1]:
                aux = lista[i]
                lista[i] = lista[i + 1]
                lista[i + 1] = aux
    return lista


def busca_binaria(lista, busca):
    inicio, fim = 0, len(lista) - 1
    while inicio <= fim:
        meio = (inicio + fim) / 2
        if busca == lista[int(meio)]:
            return True
        else:
            if lista[int(meio)] < busca:
                inicio = meio + 1
            else:
                fim = meio - 1
        return False

'''
if __name__ == '__main__':
    lista_1 = [1, 3, 4, 9, 10, 11, 15, 16, 19, 20, 22, 26, 28, 31, 33, 34]
    lista2 = [9, 8, 7, 6, 5, 4, 3, 2, 1, 33, 44, 55, 67, 44, 12, 22, 0, 5, 67, 87]

    print('Metodo de Seleção: %s ' %selecao(lista2))
    print('Metodo Bolha: %s' %bolha(lista2))
    print(busca_binaria(lista_1, 30))
'''

