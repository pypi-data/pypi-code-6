from distutils.core import setup

setup(
    name = "checkbed",
    packages = ["checkbed"],
    # scripts = ["scripts/checkcoll.py", "scripts/bedinfo.py"],
    data_files = [('/usr/local/bin', ["scripts/bedinfo", "scripts/checkcoll"])],
    version = "0.2.5",
    description = "A class for checking plink bed files",
    author = "Kaiyin Zhong",
    author_email = "kindlychung@gmail.com",
    url = "https://github.com/kindlychung/pygmail",
    keywords = ["plink", "bioinformatics", "genetics"]
    )

