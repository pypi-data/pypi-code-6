from dbfpy import dbf

db = dbf.Dbf("/home/olemb/src/files/dbf/claonilton_vieira__FPMANO24.dbf")
for rec in db:
    print(rec.asDict())
    break
