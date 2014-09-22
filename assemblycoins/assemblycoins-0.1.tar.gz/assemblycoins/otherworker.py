import time
from main import workerstuff

start=time.time()
interval=30
while True:
  if time.time()>=interval+start:
    start=time.time()
    workerstuff()
