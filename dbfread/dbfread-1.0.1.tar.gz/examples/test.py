import dbfread

t = dbfread.read('people.dbf')
print(t.deleted)
