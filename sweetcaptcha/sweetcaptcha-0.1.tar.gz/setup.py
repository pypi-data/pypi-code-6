from setuptools import setup

setup(
    name='sweetcaptcha',
    version='0.1',
    packages=['sweetcaptcha'],
    author='Jaime Wyant',
    author_email='programmer.py@gmail.com',
    description='API for easy integration of sweetcaptchas '
    '(http://sweetcaptcha.com/)',
    license='BSD',
    url='https://pypi.python.org/pypi/sweetcaptcha',
    keywords='sweetcaptcha captcha',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 2",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Widget Sets",
        "License :: OSI Approved :: BSD License"
    ],
    long_description="""\
    Sweetcaptcha Generator And Validator
    ------------------------------------

    Generates and validates sweetcaptchas (http://sweetcaptcha.com/).

    Steps to use:

      1) Create account at sweetcaptcha.com, which provides an app_id and
         app_key.
      2) Use sweetcaptcha.get_html to generate the sweetcaptcha HTML widget.
      3) Use sweetcaptcha.check to verify a posted sweetcaptcha.

    If you use wtforms, there is a SweetCaptcha widget that will simplify your
    life.  See sweetcaptcha.sweetcaptchawt for documentation.

    A demo of the library can be seen by installing Flask and wtforms.  After
    installing the required libraries run sweetcaptcha.flaskdemo.
    """
)
