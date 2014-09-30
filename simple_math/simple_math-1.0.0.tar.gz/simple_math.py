def factors(num):
    '''factors(...) -> list
    
    returns all factors of num as a list'''
    l=[]
    for x in range(int(num/2+1),1,-1):
        if num%x==0:
            l.append(x)
    l.append(1)
    return l

def mean(l):
    '''mean(...) -> float
    
    returns the Mean(Average) of a list of numbers'''
    num=0
    for x in l:
        num+=x
    num=num/len(l)
    if num%1==0:
        return int(num)
    else:
        return num

def median(l):
    '''median(...) -> float
    
    returns the Median of a list of numbers'''
    if len(l)%2==0:
        num1=l[int(len(l)/2-1)]
        num2=l[int(len(l)/2)]
        num=num1+num2
        num/=2
        if num%1==0:
            return int(num)
        else:
            return num
    else:
        num=len(l)-1
        num=int(num/2)
        num=l[num]
        return num

def mode(l,time='first'):
    '''mode(...) -> list
    
    returns the Mode(s) in a list'''
    l.sort()
    if l==list(set(l)) and time!='first':
        return l
    elif l==list(set(l)) and time=='first':
        return None
    else:
        ol=list(set(l))
        for x in ol:
            l.remove(x)
    if l==list(set(l)):
        return l
    else:
        return mode(l)

def prime(num):
    '''prime(...) -> bool
    
    returns True if num is a prime number and False otherwise'''
    if num!=1:
        val=True
    else:
        val=False
    for x in range(2,num):
        if num%x==0:
            val=False
    return val

def gcf(num1,num2):
    '''gcf(...) -> int
    
    returns the Greatest Common Factor of two numbers'''
    if num2==0:
        return num1
    else:
        return gcf(num2,num1%num2)

def gcfl(l):
    '''gcfl(...) -> int
    
    returns the Greatest Common Factor of a list of numbers'''
    def gcf(num1,num2):
        if num2==0:
            return num1
        else:
            return gcf(num2,num1%num2)
    if len(l)==1:
        return l[0]
    val=gcf(l[0],l[1])
    for x in range(2,len(l)):
        val=gcf(val,l[x])
    return val

def lcd(num1,num2):
    '''lcd(...) -> int
    
    returns the Least Common Denominator of two numbers'''
    def gcf(num1,num2):
        if num2==0:
            return num1
        else:
            return gcf(num2,num1%num2)
    return int(num1*num2/gcf(num1,num2))

def lcdl(l):
    '''lcdl(...) -> int
    
    returns the Least Common Denominator of a list of numbers'''
    def lcd(num1,num2):
        def gcf(num1,num2):
            if num2==0:
                return num1
            else:
                return gcf(num2,num1%num2)
        return int(num1*num2/gcf(num1,num2))
    if len(l)==1:
        return l[0]
    val=int(lcd(l[0],l[1]))
    for x in range(2,len(l)):
        val=lcd(val,l[x])
    return val

def psr(num):
    '''psr(...) --> bool
    
    returns true if num has a perfect square root and false otherwise'''
    from math import sqrt
    if sqrt(num)%1==0:
        return True
    return False

def pvint(num,place_value=1):
    '''pvint(...) -> int
    
    returns the place value of a number in a integer(eg... pvint(14,1) -> 4)'''
    if isinstance(num,float) or isinstance(place_value,float):
        raise ValueError('"num" or "place_value" is a float')
    if place_value>num:
        raise IndexError('"place_value" out of range')
    num=str(num)
    pv=str(place_value)
    l=[]
    for x in num:
        l.append(x)
    l.reverse()
    return int(l[len(pv)-1])

def pvfloat(num,place_value=1.0):
    '''pvfloat(...) -> int
    
    returns the place value of a number in a float(eg... pvfloat(54.0,10.0))
    -> 5'''
    if isinstance(num,int) or isinstance(place_value,int):
        raise ValueError('"num" or "place_value" is an int')
    n=[]
    pv=[]
    n.extend(str(num).split('.'))
    pv.extend(str(place_value).split('.'))
    if len(pv[0])> len(n[0]) or len(pv[1])>len(n[1]):
        raise IndexError('"place_value" out of range')
    if len(pv[0])>1:
        number=n[0][-1*(len(pv[0]))]
        return int(number)
    elif len(pv[1])>1:
        number=n[1][len(pv[1])]
        return int(number)
    else:
        if pv[0]==1:
            number=n[0][-1]
            return int(number)
        else:
            number=n[1][0]
            return int(number)

def prifac(num):
    '''prifac(...) -> list
    
    returns the Prime Factorization of num in a list'''
    def split(num):
        if num==2:
            return num
        if num%2==0:
            return [split(int(num/2)),2]
        for x in range(3,int(num/3)+2,2):
            if num%x==0:
                return [split(int(num/x)),x]
        return num
    def remove(l):
        if isinstance(l,int):
            if l!=1:
                return [l]
            return []
        ol=[]
        for x in l:
            if isinstance(x,list):
                ol.extend(remove(x))
            else:
                ol.append(x)
        return ol
    return remove(split(num))

def exno(num):
    '''exno(...) -> string
    
    returns the Expanded Notation in a a string'''
    string=''
    num=str(num)
    index=int(pow(10,len(num))/10)
    for x in num:
        if x=='0':
            index/=10
            continue
        string+='('+str(index)+' * '+x+') + '
        index/=10
    string=string.rstrip(' + ')
    return string
