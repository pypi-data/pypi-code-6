import DBConnectionHandler
import os


# # TEST 1 : Connect to MySql
cur = DBConnectionHandler.startCon(hostname="localhost",username="root",password="password",dbname="treeofwords",autocommit=True,databaseType="mysql")
cur.execute("SELECT * FROM treeofwords.UserAuth")
data = cur.fetchall()
print str(data)				
print "\nConnection established and data transfer succesfull."

# #TEST 2 : Connect to PostgreSql -- POSTPONED
# # TEST 3 : Connect to sqlite3
cur = DBConnectionHandler.startCon(dbname= os.path.dirname(os.path.abspath(__file__))+"\HashTagDB.db",autocommit=True,databaseType="sqlite3")
cur.execute("CREATE TABLE TES(TABLE\
   ID INT PRIMARY KEY     NOT NULL,\
   NAME           TEXT    NOT NULL,\
   AGE            INT     NOT NULL,\
   ADDRESS        CHAR(50),\
   SALARY         REAL\
);")

cur.execute("INSERT INTO COMPANY VALUES (1,'NAME','10','sd','213')");
data = cur.execute("SELECT * from COMPANY")
for row in data:
	print row

print "\nConnection established and data transfer succesfull."