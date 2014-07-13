from setuptools import setup


setup(
    name='eyes_on_me',
    version='0.5',
    packages=['eyes_on_me'],
    scripts=['eyes_on_me/bin/eyes_on_me'],
    description=('eyes_on_me is simple utility which allows you to '
                 'control your screen backlight and temperature according to lighting'),
    license='BSD',
    long_description='wb temperature and backlight adjuster according to ',
    install_requires=["astral",
                      "PIL",
                      "daemonize"],
    include_package_data=True,
    package_data={'shared': ["etc/.eyes_on_me_rc"]},
    author="Yuriy Netesov",
    author_email="yuriy.netesov@gmail.com",
    url="https://bitbucket.org/dehun/eyes_on_me/",
)
