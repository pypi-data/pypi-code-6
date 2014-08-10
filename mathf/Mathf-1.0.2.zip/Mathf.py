"""This module provides some basic math-functions"""
import math

def abs(Zahl):
	"""Calculates the absolut of a number"""
	if(Zahl < 0):
		return (Zahl*-1)
	else:
		return(Zahl)


def modulo (First,Second):
	"""Calculates FIRST-mod-SECOND"""
	if(First > 0):
		if(First > Second):
			modulo(First-Second,Second)
		if(First == Second):
			return (0)
		if(First < Second):
			return (First)
	else:
		modulo(First+Second,Second)

def Deg2Rad(Degree):
       """Calculates the Radians-Value from Degree"""
       Multiplier = math.pi/180
       return(Degree*Multiplier)


def Rad2Deg(Radians):
        """Calculates the Degree-Value from Radians"""
        Multiplier = 180/math.pi
        return(Radians*Multiplier)

def Ceil(f):
        """Calculates the smallest Integer-Value that remains bigger or equal to f"""
        if(f >= 0):
                Value = 0
                while(f > Value):
                        Value = Value+1
                return Value
        if(f < 0):
                Value = (math.floor(f)-10)
                while(f > Value):
                        Value = Value+1
                return Value
            
def Floor(f):
        #Calculates the biggest Integer-Value that remains smaller or equal to f
	if(f >= 0):
		Value = 0
		while(Value < f):
			Value = Value + 1
		Value = Value - 1
		return(Value)
	if(f < 0):
		Value = 0
		while(Value > f):
			Value = Value-1
		return(Value)

def Clamp(Val,Min,Max):
        """Clamps 'VAL' to 'MIN' and 'MAX'"""
        if(Val < Min):
                return Min
        if(Val > Max):
                return Max
        else:
            return Val

def cos(f):
        #Returns cos
	return math.cos(f)

def sin(f):
        #Returns sin
	return math.sin(f)

def tan(f):
        #Returns tan
	return math.tan(f)

def log(f):
        #Returns log
	return math.log(f)

def sqrt(f):
    #Returns sqrt
    return math.sqrt(f)

        



	    

        

	

