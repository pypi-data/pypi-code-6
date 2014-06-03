import gffutils
import sqlite3

fn = gffutils.example_filename('nonascii')
db = gffutils.create_db(fn, ':memory:', text_factory=sqlite3.OptimizedUnicode)

#assert db.conn.text_factory is str

# Get the last line, which has a Beta in the ID
for line in open(fn):
    pass

# Bypass the database and get attributes directly.
a, d = gffutils.parser._split_keyvals(line.split('\t')[-1])

ID = a['ID'][0]; assert type(a['ID'][0]) == str

f = db[ID]
ID2 = f['ID'][0]
assert type(ID2) == unicode

assert type(f['evidence'][0]) is str

