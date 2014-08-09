"""Beinhaltet grundlegende mathematische Berechnungsfunktionen"""
import math

def abs(Zahl):
	"""Berechnet den Betrag einer Zahl"""
	if(Zahl < 0):
		print (Zahl*-1)
	else:
		print(Zahl)


def modulo (First,Second):
	"""Berechnet A-Mod-B mit den Parametern A und B"""
	if(First > 0):
		if(First > Second):
			modulo(First-Second,Second)
		if(First == Second):
			print (0)
		if(First < Second):
			print (First)
	else:
		modulo(First+Second,Second)

def Deg2Rad(Degree):
       """Berechnet den Radiant-Wert aus dem Degree-Parameter"""
       Multiplier = math.pi/180
       print(Degree*Multiplier)


def Rad2Deg(Radians):
        """Berechnet den Degree-Wert aus dem Radiant-Parameter"""
        Multiplier = 180/math.pi
        print(Radians*Multiplier)

def Ceil(f):
        """Berechnet den kleinsten Integer-Wert der größer oder gleich f ist"""
        if(f >= 0):
                Value = 0
                while(f > Value):
                        Value = Value+1
                print(Value)
        if(f < 0):
                Value = (math.floor(f)-10)
                while(f > Value):
                        Value = Value+1
                print(Value)

        

	

