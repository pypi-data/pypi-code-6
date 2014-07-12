"""This is a function which can tell a number is prime number or not"""
def isprime(number):
        count=2
        while count<number:
            if number%count==0:
                print("Not a prime number")
                break
            else:
                count=count+1
                print("It's a prime number")
