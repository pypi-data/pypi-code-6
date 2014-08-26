#coding=utf-8

def how_many( n ):
    a = [0]
    def tell_me( n=n ):
        a[0] = (a[0] + 1) % n
        return a[0]
    return tell_me