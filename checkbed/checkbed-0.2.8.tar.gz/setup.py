from distutils.core import setup

import platform, os
sysname = platform.system()
if sysname == "Windows":
    binpath = os.getenv("SystemRoot")
else:
    binpath = r"/usr/local/bin"

setup(
    name = "checkbed",
    packages = ["checkbed"],
    # scripts = ["scripts/checkcoll.py", "scripts/bedinfo.py"],
    data_files = [(binpath, ["scripts/bedinfo", "scripts/checkcoll"])],
    version = "0.2.8",
    description = "A class for checking plink bed files",
    author = "Kaiyin Zhong",
    author_email = "kindlychung@gmail.com",
    url = "https://github.com/kindlychung/pygmail",
    keywords = ["plink", "bioinformatics", "genetics"]
    )

