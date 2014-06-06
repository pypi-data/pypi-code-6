from setuptools import setup, find_packages
from iam_syncr import VERSION

setup(
      name = "iam_syncr"
    , version = VERSION
    , packages = ['iam_syncr'] + ['iam_syncr.%s' % pkg for pkg in find_packages('iam_syncr')]
    , include_package_data = True

    , install_requires =
      [ "rainbow_logging_handler"
      , "pyYaml"
      , "boto"
      ]

    , extras_require =
      { "tests":
        [ "noseOfYeti>=1.5.1"
        , "nose"
        , "mock"
        ]
      }

    , entry_points =
      { 'console_scripts' :
        [ 'iam_syncr = iam_syncr.executor:main'
        ]
      }

    # metadata for upload to PyPI
    , author = "Stephen Moore"
    , author_email = "stephen@rea-group.com"
    , description = "Syncs iam roles"
    , license = "MIT"
    , keywords = "iam amazon credentials"
    )
