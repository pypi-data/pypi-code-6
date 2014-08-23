# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        TesteFinDt
# Purpose:  Permite a realização de vários testes com o módulo FinDt, os quais
#       já podem servir como exemplo do seu uso.
#
# Author:      Marcelo
#
# Created:     16/08/2014
# Copyright:   (c) Marcelo 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

# Python module


# Own modules
import FinDt

__author__ = """\n""".join(['Marcelo G Facioli (mgfacioli@yahoo.com.br)'])
__version__ = "3.0.0"


def main():
    """

    :rtype : object
    """
    var_path = "C:\\Apostilas\\Python\\BCB\\feriados_nacionais.csv"  ## Home Version

    print("\n***Teste*** a:\n")
    dt_ini = '01/01/2013'
    dt_fim = '28/02/2013'

    a = FinDt.DatasFinanceiras(dt_ini, dt_fim, opt=1, path_arquivo=var_path)
    print(type(a))
    print(a)
    dt1 = a.dias()
    print(len(dt1))
    dt1 = a.dias(opt=2)
    print(len(dt1))
    dt1 = a.dias(opt=3)
    print(len(dt1))
    print(a.lista_feriados())
    print(a.dias_uteis_por_mes())
    print(a.lista_dia_especifico_semana(3))


    print("\n***Teste*** b:\n")
    b = FinDt.DatasFinanceiras('01-11-2013', '31-12-2013', path_arquivo=var_path)

    # for j in [b, type(b)]:
    #     print("{}\n".format(j))
    #
    # for i in range(1, 4):
    #     dt1 = b.Dias(Opt=i)
    #     print("{}\n{}\n".format(len(dt1),dt1))

    print("Dias corridos do periodo selecionado:")
    dt1 = b.dias()
    print("\tTamanho da lista: {} dias.".format(len(dt1)))
    print("\tLista de dias: {}".format(dt1))
    print("\tTipo: {}\n".format(type(dt1)))

    print("Dias uteis sem feriados do periodo selecionado:")
    dt2 = b.dias(opt=2)
    print("\tTamanho da lista: {} dias.".format(len(dt2)))
    print("\tLista de dias: {}\n".format(dt2))

    print("Dias uteis com feriados do periodo selecionado:")
    dt3 = b.dias(opt=3)
    print("\tTamanho da lista: {} dias.".format(len(dt3)))
    print("\tLista de dias: {}\n".format(dt3))


    print("Lista de Feriados dentro do periodo selecionado:")
    for dia in b.lista_feriados():
        print("\tDia: {}, feriado: {}".format(dia, b.lista_feriados()[dia]))

    print("Todos Domingos dentro do período selecionado: \n\t{}\n".format(b.lista_dia_especifico_semana(7)))
    print("Todas quartas-feiras dentro do período selecionado: \n\t{}\n".format(b.lista_dia_especifico_semana(3)))

    print("")

    print("Primeiro e último dia do mês de um dia qualquer (o dia não precisar estar dentro do período selecionado")
    for dia in ['15/11/2013', '22/12/2013', '08/02/2014']:
        print("\tDia: {} e Dia da semana: {}".format(dia, b.dia_semana(dia)))
        print("\tPrimeiro: {} e ultimo: {}\n".format(b.primeiro_dia_mes(dia), b.ultimo_dia_mes(dia)))

    print("Lista de dias uteis mensal do periodo selecionado:")
    for mes in b.dias_uteis_por_mes():
        print("\tMes/Ano: {} - dias uteis: {}".format(mes, b.dias_uteis_por_mes()[mes]))

    print("Criando um subperiodo do periodo principal:")
    for i in range(1, 4):
        sub = b.subperiodo("10/11/2013", "23/12/2013", opt=i)
        print("\tTamanho da lista: {} dias.".format(len(sub)))
        print("\tLista de dias: {}".format(sub))
        print("\tTipo: {}\n".format(type(sub)))


    cj1 = {}


if __name__ == '__main__':
    main()






