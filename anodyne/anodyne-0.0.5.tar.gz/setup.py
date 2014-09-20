from setuptools import setup


VERSION = (0, 0, 5, "")

requirements = [
    "SQLAlchemy==0.9.7"
]

setup(
    name="anodyne",
    description="SQLAlchemy Database Utilities",
    packages=["anodyne"],
    version=".".join(filter(None, map(str, VERSION))),
    author="Alex Milstead",
    author_email="alex@amilstead.com",
    maintainer="Alex Milstead",
    maintainer_email="alex@amilstead.com",
    url="https://github.com/amilstead/anodyne",
    keywords=["sqlalchemy"],
    install_requires=requirements,
    package_dir={"anodyne": "anodyne"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Topic :: Database ",
        "License :: OSI Approved :: GNU General Public License (GPL)"
    ],
)
