m=0
while m==0:
    x=int(input("Is this a prime number:"))
    n=2
    while n<=x:
        if x!=n and x%n==0:
            print( x,"is not a prime number.")
            n=x+1
        elif x%n!=0 and x!=n:
            n=n+1
        elif x==n:
            print(x,"is a prime number")
            n=n+1
        
           
       
            
        
