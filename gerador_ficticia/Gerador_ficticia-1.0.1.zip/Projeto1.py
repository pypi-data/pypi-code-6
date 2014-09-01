__author__ = 'Jeferson de Souza'

from calculos import *
import random

HNO3 = 58.3
CACO3 = 99.9
NO3 = 65.8

# Fator de corre????????????????o
SODA = 1.0751
EDTA = 0.8
HCL = 0.9756

# Volumes dos tanques
Acido = 2900
Coagulante = 3900
Composto = 0
Talco = 2000
file_name = 'Calculos.txt'


def calculo_solucao(nome, arquivar_op=0):
    print('Calculo solido %s' % nome)
    parametro_up = float(input('Valor minimo: '))
    parametro_dow = float(input('Valor maximo: '))
    quantidade = int(input('Quantos calculos gostaria: '))

    if arquivar_op == 1:
        file_tes = open(file_name, 'a+')
        print('\n\n Calculo solido %s' % nome, file=file_tes)
        for i in range(quantidade):
            placa1_a = sort_num(66.001, 101.992)
            placa1_b = sort_num(66.001, 101.992)

            amostra_a = sort_num(1.500, 2.500)
            amostra_b = sort_num(1.500, 2.500)

            resultado_a = sort_num(parametro_dow, parametro_up)  # trocar pelo parametro
            resultado_b = sort_num(parametro_dow, parametro_up)  # trocar pelo parametro

            placa3a = find_c(resultado_a, amostra_a, placa1_a)
            placa3b = find_c(resultado_b, amostra_b, placa1_b)

            print('|%.3f' % placa1_a, '\t', '%.3f|' % placa1_b, file=file_tes)
            print('|%.3f' % amostra_a, '\t\t', '%.3f|' % amostra_b, file=file_tes)
            print('|%.3f' % placa3a, ' \t', '%.3f|' % placa3b, file=file_tes)
            print('|%.1f' % resultado_a, '\t\t', '%.1f|' % resultado_b, file=file_tes)
            print('|\t (%.1f)' % ((resultado_a + resultado_b) / 2), file=file_tes)
            print('---------------------', file=file_tes)
        file_tes.close()
    for i in range(quantidade):
        placa1_a = sort_num(66.001, 101.992)
        placa1_b = sort_num(66.001, 101.992)

        amostra_a = sort_num(1.500, 2.500)
        amostra_b = sort_num(1.500, 2.500)

        resultado_a = sort_num(parametro_dow, parametro_up)  # trocar pelo parametro
        resultado_b = sort_num(parametro_dow, parametro_up)  # trocar pelo parametro

        placa3a = find_c(resultado_a, amostra_a, placa1_a)
        placa3b = find_c(resultado_b, amostra_b, placa1_b)

        print('|%.3f' % placa1_a, '\t',    '%.3f|' % placa1_b)
        print('|%.3f' % amostra_a, '\t\t', '%.3f|' % amostra_b)
        print('|%.3f' % placa3a, '\t',    '%.3f|' % placa3b)
        print('|%.1f' % resultado_a, '\t\t ',  '%.1f|' % resultado_b)
        print('|%.1f' % ((resultado_a + resultado_b) / 2))
        print('----------------------')


def calculo_nitrato(nome, arquivar_op=0):
    print('\n\n Calculo de concentra????????o %s' % nome)
    parametro_no3_a = float(input('Valor Minimo: '))
    parametro_no3_b = float(input('Valor Maximo: '))
    quantidade = int(input('Quantos calculos gostaria: '))

    if arquivar_op == 1:
        file_tes = open(file_name, 'a+')
        print('Calculo de concentra????????o %s' % nome, file=file_tes)

        for i in range(quantidade):
            print('NO3', file=file_tes)
            resultado_no3 = sort_num(parametro_no3_a, parametro_no3_b)  # trocar pelo parametro
            volume_edta = resultado_no3 / EDTA
            print('|%.1f|' % volume_edta, file=file_tes)
            print('|%.1f|' % resultado_no3, file=file_tes)
            print('--------', file=file_tes)
        file_tes.close()

    for i in range(quantidade):
        print('NO3')
        resultado_no3 = sort_num(parametro_no3_a, parametro_no3_b)  # trocar pelo parametro
        volume_edta = resultado_no3 / EDTA
        print('|%.1f|' % volume_edta)
        print('|%.1f|' % resultado_no3)
        print('--------')


def calculo_acido(nome, arquivar=0):
    print('\n\nCalculo concentra????ao de %s' % nome)
    quantidade = int(input('Quantos calculos gostaria: '))

    if arquivar == 1:
        file_tes = open(file_name, 'a+')
        print('Calculo concentra????ao de %s' % nome, file=file_tes)
        for i in range(quantidade):
            peso = sort_num(3501, 4000)
            volume = reverse_ac(sort_num(1.0, 1.4), sort_num(3500, 4100), SODA)
            print('|%d|' % peso, file=file_tes)
            print('|%.1f|' % volume, file=file_tes)
            print('|%.1f|' % analise_ac(volume, peso, SODA), file=file_tes)
            print('--------', file=file_tes)
        file_tes.close()

    for i in range(quantidade):
        peso = sort_num(3501, 4000)
        volume = reverse_ac(sort_num(1.0, 1.4), sort_num(3500, 4100), SODA)
        print('|%d|' % peso)
        print('|%.1f|' % volume)
        print('|%.1f|' % analise_ac(volume, peso, SODA))
        print('--------')

def calculo_carbonato(nome, arquivar_op=0):
    print('\n\n Calculo solido %s' % nome)
    parametro_up = float(input('Valor minimo: '))
    parametro_dow = float(input('Valor maximo: '))
    quantidade = int(input('Quantos calculos gostaria: '))

    if arquivar_op == 1:
        file_tes = open(file_name, 'a+')
        print('\n\n Calculo solido %s' % nome, file=file_tes)
        for i in range(quantidade):
            placa1_a = sort_num(0.099, 2.990)
            placa1_b = sort_num(0.099, 2.990)

            amostra_a = sort_num(12.000, 14.000)
            amostra_b = sort_num(12.000, 14.000)

            resultado_a = sort_num(parametro_dow, parametro_up)  # trocar pelo parametro
            resultado_b = sort_num(parametro_dow, parametro_up)  # trocar pelo parametro

            placa3a = find_c(resultado_a, amostra_a, placa1_a)
            placa3b = find_c(resultado_b, amostra_b, placa1_b)

            print('|%.3f|' % placa1_a, ' | ', '%.3f|' % placa1_b, file=file_tes)
            print('|%.3f|' % amostra_a, ' | ', '%.3f|' % amostra_b, file=file_tes)
            print('|%.3f|' % placa3a, ' | ', '%.3f|' % placa3b, file=file_tes)
            print('|%.1f|' % resultado_a, ' | ', '%.1f|' % resultado_b, file=file_tes)
            print('|%.1f|' % ((resultado_a + resultado_b) / 2), file=file_tes)
            print('-----------------------', file=file_tes)
        file_tes.close()
    for i in range(quantidade):
        placa1_a = sort_num(0.099, 2.990)
        placa1_b = sort_num(0.099, 2.990)

        amostra_a = sort_num(12.000, 14.000)
        amostra_b = sort_num(12.000, 14.000)

        resultado_a = sort_num(parametro_dow, parametro_up)  # trocar pelo parametro
        resultado_b = sort_num(parametro_dow, parametro_up)  # trocar pelo parametro

        placa3a = find_c(resultado_a, amostra_a, placa1_a)
        placa3b = find_c(resultado_b, amostra_b, placa1_b)

        print('|%.3f|' % placa1_a, ' |', '%.3f|' % placa1_b)
        print('|%.3f|' % amostra_a, ' |', '%.3f|' % amostra_b)
        print('|%.3f|' % placa3a, ' |', '%.3f|' % placa3b)
        print('|%.1f|' % resultado_a, ' |', '%.1f|' % resultado_b)
        print('|%.1f|' % ((resultado_a + resultado_b) / 2))
        print('-----------------------')


if __name__ == '__main__':
    print('-----------------------------------')
    print('|Gerador de Calculos Ficticios.    |')
    print('|V -  1.0.2                        |')
    print('|Desenvolvido por: Jeferson S.     |')
    print('|Email: mp_bra_nco@hotmail.com     |')
    print('-----------------------------------')



    solucao = 1000
    while solucao != 0:
        print('Escolha uma OP: ')
        print('[1] - Ctf-3f')
        print('[2] - Talco')
        print('[3] - Composto')
        print('[4] - Polimero')
        print('[5] - Acido')
        print('[6] - Nitrato')
        print('[7] - Cabonato')
        print('[0] - SAIR')

        solucao = int(input('Opcao: '))
        if solucao == 0:
            break
        salvar_op = input('Deseja Gerar um txt?  [s/n]: ')
        salvar_op = salvar_op.upper()
        op_num = 0

        if salvar_op == 'S':
            op_num = 1
        elif salvar_op == 'N':
            op_num = 2
        else:
            print('Valor invalido, somento [S =  Sim | N = N??o]')

        if solucao == 1:
            nome = 'CTF-3F'
            if salvar_op == 'S':
                calculo_solucao(nome, op_num)
            else:
                calculo_solucao(nome, op_num)

        elif solucao == 2:
            nome = 'Talco'
            if salvar_op == 'S':
                calculo_solucao(nome, op_num)
            else:
                calculo_solucao(nome)

        elif solucao == 3:
            nome = 'Composto'
            if salvar_op == 'S':
                calculo_solucao(nome, op_num)
            else:
                calculo_solucao(nome)

        elif solucao == 4:
            nome = 'Polimero'
            if salvar_op == 'S':
                calculo_solucao(nome, op_num)
            else:
                calculo_solucao(nome)

        elif solucao == 5:
            nome = 'Acido'
            if salvar_op == 'S':
                calculo_acido(nome, op_num)
            else:
                calculo_acido(nome)

        elif solucao == 6:
            nome = 'Nitrato'
            if salvar_op == 'S':
                calculo_nitrato(nome, op_num)
            else:
                calculo_nitrato(nome)

        elif solucao == 7:
            nome = 'Carbonato'
            if salvar_op == 'S':
                calculo_carbonato(nome, op_num)
            else:
                calculo_carbonato(nome)

        else:
            print('Valor Inv??lido!! \n\n')


