import subprocess
import sys

wget_output = "" # buffer to hold the result

p = subprocess.Popen("wget http://example.com",shell=True,stdout=subprocess.PIPE,stderr=stdout)

# Keep trying to read 1 char at a time until the process ends 
# poll() returns None while  the process is still running
while p.poll() is None:
    char = p.stderr.read(1)
    if char:
        sys.stdout.write(char)
        wget_output += char
    
# Read any remainder that might not have been read in the loop
remainder = p.stderr.read()
sys.stdout.write(remainder)
wget_output += remainder

