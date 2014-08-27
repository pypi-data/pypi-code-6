from setuptools import setup, find_packages
setup(
    name="mongosion",
    version="0.10",
    description="A session moudel for tornado using mongodb",

    author="xiaocao",
    author_email = "xiaocao.grasses@gmail.com",

    url="https://github.com/grasses/mongosion",
    license = "GPL",
    packages= find_packages(),
    scripts=["demo/test.py"],
    keywords = ("mongodb", "tornado", "mongosion"),
)



