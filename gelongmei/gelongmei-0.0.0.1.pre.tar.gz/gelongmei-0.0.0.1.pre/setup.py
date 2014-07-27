from setuptools import setup

setup(
      name='gelongmei',
      version='0.0.0.1 pre',
      packages=['gelongmei'],
      author='gelongmei',
      author_email='gelongmei@qq.com',
      license='LGPL',
      install_requires=["PyYAML>=3.10","Markdown>=2.1.1","tornado>=2.2"],
      description="A HTML5 Slide Generator in python",
      entry_points ={
        'console_scripts':[
            'SlideGen=slidegen.SlideGen:Main'
        ]
      },
      keywords ='html5 slide generator',
      url='https://github.com/babyladyyyn/fsmpython'
)
