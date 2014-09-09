from bam2x.Annotation import H_VCF,F_VCF
from bam2x.DBI.Templates import sqlite3_template_factory
schema,insert=sqlite3_template_factory(H_VCF,F_VCF)
import sqlite3
conn=sqlite3.connect("test.db")
cursor=conn.cursor()
cursor.execute(schema.substitute({"table_name":"test"}))
print insert.substitute({"table_name":"test"})
cursor.executemany(insert.substitute({"table_name":"test"}),[("chr1",200,"testvcf","A","C",40,"a","test")])

conn.commit()
