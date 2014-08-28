"""BootF2.py
   Farandole 2 bootstrapper: builds the kernel using information from metadict.py
   ------------------------
 	(note: code has moved into F2 package: OFF_boot.py)
   Th. Estier
   version 0.1 - 3 sept 2003
 """
import sys
from F2 import OFFboot

# database_url = 'file:root.db'
database_url = 'rpc:127.0.0.1:8080'
if len(sys.argv) > 1:
	database_url = sys.argv[1]

OFFboot.main(database_url)
