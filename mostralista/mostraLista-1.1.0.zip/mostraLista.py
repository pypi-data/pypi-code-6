""" modulo que fornece uma funcao mostraLista()
que imprime listas que podem ou nao ser aninhadas """
def mostraLista(lista, n_tab):

    """ 'lista' eh um elemento posicional que pode ser
    qualquer lista. Cada item na lista (com possiveis)
    listas aninhadas) eh impressa em uma linha, e 'n_tab'
    eh usado para inserir tabulacoes quando uma lista
    aninhada eh encontrada """
    for item in lista:
        #se 'item' for do tipo list
        if isinstance(item, list):
            mostraLista(item, n_tab+1)

        else:
            #'n_tab' controla o numero de tabulacoes a serem usadas
            for tab_stop in range(n_tab):
                #exibe um caractere de tabulacao para cada nivel de recuo
                print("\t", end='')

            print(item)
