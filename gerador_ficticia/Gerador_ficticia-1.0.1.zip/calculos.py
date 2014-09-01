__author__ = 'Jeferson de Souza'


#Arquivos de funçoes predifinidas.

#ajustes ---------------
import random

def ajust_up(result, volume, concentracao, limite):
    return ((limite - result) * volume) / concentracao


def ajust_down(result, volume_TQ, limite):
    return ((result * volume_TQ) / limite) - volume


#analises---------------------
def analise_ac(volume, peso_amos, FC):
    return (volume * FC * 63 * 100) / peso_amos


def analise_coag(result, reagente):
    return result * reagente


#solidos
def solido(valor_a, valor_b, valor_c):
    return ((valor_c - valor_a) / valor_b) * 100


#Calculos reversos -----------------------------------

def find_c(valor_d, valor_b, valor_a):
    return ((valor_d / 100) * valor_b) + valor_a


def reverse_ac(esperado = 1.0, peso = 1, FC = 0):
    return (esperado * peso)/(FC * 6300)

#Arquivar------------------------------

def arquivar_analises(result, nome):
    file = open('resultados_analises.txt', 'a')
    file.write('\n\n Analise de %s \n' % nome)
    file.write('Resultado %2.2f' % result)
    file.close()
#-----------------
def salvar(nome_file, dados):
    files = open(nome_file, 'w+')
    print(dados, file=files)
    files.close()
#-----------------
#Numeros aleatorios ---------------------------

def sort_num(piso = 1, teto = 1):
    if type(piso) == int:
        return random.randint(piso, teto)
    elif type(piso):
        return random.uniform(piso, teto)



