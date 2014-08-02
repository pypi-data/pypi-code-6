import zipfile
import sys
from urllib import request


#cloneCMD(cmd_user_name, cmd_repo_name)

def clone(user_name, repo_name):

	"""
	For Direct Runnig
	user_name = input("Enter GitHub Username: ")
	repo_name = input("Enter GitHub Repo name: ")
	"""
	zip_name = "master.zip"

	url = "https://github.com/%s/%s/archive/master.zip" % (user_name, repo_name)

	#print(url) ok it works!
	try:
		print("\nSearching repo...")
		request.urlretrieve(url, zip_name)


		print("\nCloned repository. List of repository content..\n")

		zf = zipfile.ZipFile(zip_name, "r")

		for foldername in zf.namelist():
			print(foldername)

		print("\nExtract Archive Content...")

		with zipfile.ZipFile(zip_name, "r") as zfile:
			zfile.extractall()

	except request.URLError as e:
		if e.code == 404:
			print("Repository not found. Check Github Username and Repository Name")