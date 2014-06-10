def ListaAninhadaIterativa(lista):
    for each_item in lista:
        if isinstance(each_item, list):
            ListaAninhadaIterativa(each_item)
        else:
            print(each_item)
