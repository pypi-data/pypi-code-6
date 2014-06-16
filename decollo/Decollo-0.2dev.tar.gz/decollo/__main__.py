import installs
import subprocess

subprocess.call("clear", shell=True)
steamAnswer = raw_input("Install Steam? (y/n)")

installs.steam(steamAnswer)
