from setuptools import setup

setup(
    name='Usurper',
    version='0.9.0',
    author='Thomas Proisl',
    author_email='thopro@posteo.de',
    packages=[
        'usurper',
        'usurper.utils',
    ],
    scripts=[
        'bin/usrpr',
    ],
    package_data={
        'usurper': ["data/ar-padt.map", "data/bg-btb.map", "data/ca-cat3lb.map", "data/cs-pdt.map", "data/da-ddt.map", "data/de-negra.map", "data/de-tiger.map", "data/el-gdt.map", "data/en-brown.map", "data/en-ptb.map", "data/en-tweet.map", "data/es-cast3lb.map", "data/eu-eus3lb.map", "data/fi-tdt.map", "data/fr-paris.map", "data/hu-szeged.map", "data/it-isst.map", "data/iw-mila.map", "data/ja-kyoto.map", "data/ja-verbmobil.map", "data/ko-sejong.map", "data/nl-alpino.map", "data/pl-ipipan.map", "data/pt-bosque.map", "data/ru-rnc.map", "data/sl-sdt.map", "data/sv-talbanken.map", "data/tu-metusbanci.map", "data/zh-ctb6.map", "data/zh-sinica.map"]
    },
    url='http://pypi.python.org/pypi/Usurper/',
    license='GNU General Public License v3 or later (GPLv3+)',
    description='An unsupervised dependency parser.',
    long_description=open('README.txt').read(),
    install_requires=[
        "networkx",
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Text Processing :: Linguistic',
    ],
)
