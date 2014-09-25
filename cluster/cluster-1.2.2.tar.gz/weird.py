def foo():
    for i in range(10):
        yield i


gen = foo()
try:
    while True:
        print(next(gen))
        print(next(gen))
except StopIteration:
    pass


print('------------------')

gen2 = foo()
while True:
    a = next(gen2)
    b = next(gen2)
    print(a)
    print(b)
