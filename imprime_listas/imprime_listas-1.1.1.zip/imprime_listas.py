def imprime_listas(lista,level=0):
    for i in lista:
        if isinstance(i,list):
            imprime_listas(i,level+1)
        else:
            for tab_stop in range(level):
                print("\t", end='')
            print(i)
