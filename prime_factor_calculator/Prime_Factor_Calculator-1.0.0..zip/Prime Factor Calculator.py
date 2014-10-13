m=0
while m==0:
    x=int(input("Find prime factors of: "))
    n=2
    while(n<=x):
        if x%n==0:
            print(n)
            x=x/n
        else:
            n=n+1
        
            
