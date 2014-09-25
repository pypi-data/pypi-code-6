def test(data):
    data.append(1)
    yield data
    data.append(2)
    yield data


data = [0, 0, 0, 0]
print data
for row in test(data):
    print row
print data
