import whoispy
import sys

argvs = sys.argv
argc = len(argvs)

if (argc != 2):
	print "Bad argument"
	quit()

hoge = whoispy.Query(argvs[1])
print hoge.get_raw_data()
print hoge.get_vacant_bool()
