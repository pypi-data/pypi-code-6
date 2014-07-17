import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='UMorpheme',
    version='1.0.3',
    license="MIT License",
    keywords="Korean Morpheme Analyzer",
    packages=['Umorpheme'],
    url="http://newsjam.kr",
    author="Kyunghoon Kim",
    author_email="kyunghoon@unist.ac.kr",
    description="Online Korean Morpheme Analyzer with Eunjeon Hannip Project(eunjeon.blogspot.kr). Actually, this is for high school students who do not use the linux.",
    long_description=read('README'),
)