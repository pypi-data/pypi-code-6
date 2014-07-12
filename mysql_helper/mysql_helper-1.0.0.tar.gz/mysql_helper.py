# -*- coding: utf8 -*-
import MySQLdb
import MySQLdb.cursors

"""
    Este é o módulo mysql_helper que fornece métodos que auxiliam em operações com o MySQL utilizando a biblioteca MySQLdb

"""



def connectDB(user, password, host='localhost', db=None):
    """Este método realiza a conexão com o banco.
    
    user -- Nome de usuário para conectar ao banco. (Obrigatório)
    password -- Senha de acesso do usuário. (Obrigatório)
    host -- Endereço onde está hospedado o MySQL. (Opcional - Padrão localhost)
    db -- Nome do banco que deseja conectar. (Opcional - Padrão None)
    
    Retorna a conexão com o banco
    
    """
    cursor = MySQLdb.cursors.DictCursor
    
    conn = MySQLdb.connect(host=host, user=user, passwd=password, cursorclass=cursor)
    
    return conn.cursor()
    
    


def executeSelect(comandoSQL, cursor):
    """
        Método que realiza a execução de uma consulta SQL.
    
        comandoSQL -- A query da select que será executada. (Obrigatório)
        cursor -- O cursor para executar a SQL
        
        Retorna o resultado da consulta utilizando o DictCursor.
        
    """
    
    result = cursor.execute(comandoSQL)
    return result


def executeInsert(comandoSQL, cursor):
    
    """
        Método que realiza a execução de uma inserção.
    
        comandoSQL -- A query de insert que será executada. (Obrigatório)
        cursor -- O cursor para executar a SQL
        
        Retorna TRUE ou FALSE.
        
    """
    
    if comandoSQL.upper().startswith('INSERT'):
        try:
            cursor.execute(comandoSQL)
            return True
        except Exception, erro:
            print "Ocorreu o seguinte erro ao executar o INSERT: %s", erro
            return False
    else:
        print "O string SQL não é um comando de insert."
        return False
    

    
    
def executeUpdate(comandoSQL, cursor):
    
    """
        Método que realiza a execução de uma alteração.
    
        comandoSQL -- A query de update que será executada. (Obrigatório)
        cursor -- O cursor para executar a SQL
        
        Retorna TRUE ou FALSE.
        
    """
    
    if comandoSQL.upper().startswith('UPDATE'):
        try:
            cursor.execute(comandoSQL)
            return True
        except Exception, erro:
            print "Ocorreu o seguinte erro ao executar o UPDATE: %s", erro
            return False
    else:
        print "O string SQL não é um comando de insert."
        return False

def executeDelete(comandoSQL, cursor):
    
    """
        Método que realiza a execução de uma exclusão.
    
        comandoSQL -- A query de delete que será executada. (Obrigatório)
        cursor -- O cursor para executar a SQL
        
        Retorna TRUE ou FALSE.
        
    """
    
    if comandoSQL.upper().startswith('DELETE'):
        try:
            cursor.execute(comandoSQL)
            return True
        except Exception, erro:
            print "Ocorreu o seguinte erro ao executar o DELETE: %s", erro
            return False
    else:
        print "O string SQL não é um comando de insert."
        return False

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    