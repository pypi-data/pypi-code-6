from setuptools import setup, find_packages
from credo import VERSION

setup(
      name = "credo_manager"
    , version = VERSION
    , packages = ['credo'] + ['credo.%s' % pkg for pkg in find_packages('credo')]
    , include_package_data = True

    , install_requires =
      [ "rainbow_logging_handler"
      , "pycrypto"
      , "paramiko>=1.14.0"
      , "requests"
      , "keyring"
      , "pygit2"
      , "boto"
      ]

    , extras_require =
      { "tests":
        [ "noseOfYeti>=1.5.0"
        , "nose"
        , "mock"
        ]
      }

    , entry_points =
      { 'console_scripts' :
        [ 'credo = credo.executor:main'
        ]
      }

    # metadata for upload to PyPI
    , url = "http://credo.readthedocs.org"
    , author = "Stephen Moore"
    , author_email = "stephen@delfick.com"
    , description = "Manager for aws credentials"
    , license = "MIT"
    , keywords = "iam amazon credentials"
    )
