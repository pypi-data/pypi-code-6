import subprocess

def steam(x):
	if x == "y" or x == "Y":
		subprocess.call("sudo apt-get install steam", shell=True)


