"""Beinhaltet grundlegende mathematische Berechnungsfunktionen"""

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