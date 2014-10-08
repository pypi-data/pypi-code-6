def zip(a,b,c):
    result = []
    result = [(a[x],b[x]) for x in range(len(a)) if len(a) == len(b)]
    if len(a) > len(b):
        for x in range(len(a)):
            if x > len(b)-1:
                result.append((a[x], c))                
            else:
                result.append((a[x], b[x]))
    if len(b) > len(a):
        for x in range(len(b)):
            if x > len(a)-1:
                result.append((c, b[x]))
            else:
                result.append((a[x], b[x]))
    return result
print zip([1,2,3],[4,5,6],"a")
print zip([1,2,3],[4],"b")
print zip([3],[5,6,7],"t")