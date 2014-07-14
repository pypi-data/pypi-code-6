""" modulo que fornece uma funcao mostraLista()
que imprime listas que podem ou nao ser aninhadas """
def mostraLista(lista):

    """ 'lista' eh um elemento posicional que pode ser
    qualquer lista. Cada item na lista (com possiveis)
    listas aninhadas) eh impressa em uma linha """
    for item in lista:
        #se 'item' for do tipo list
        if isinstance(item, list):
            mostraLista(item)

        else:
            print(item)
