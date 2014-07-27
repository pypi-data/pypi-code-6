"""
Contains function which can be used to list all prime numbers up to a given number N,
Use case
prime(n)
"""

def primes(n):
    sieve = [True]*(n+1)
    for i in range(2, n+1):
        if sieve[i]:
            print i
            for q in range(i, n+1, i):
                sieve[q] = False
