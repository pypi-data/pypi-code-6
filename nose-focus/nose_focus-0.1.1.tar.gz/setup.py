from setuptools import setup, find_packages

setup(
      name = "nose_focus"
    , version = "0.1.1"
    , packages = ['nose_focus'] + ['nose_focus.%s' % pkg for pkg in find_packages('nose_focus')]
    , include_package_data = True

     , install_requires =
       [ 'six'
       ]

    , extras_require =
      { "tests":
        [ "nose"
        , "noseOfYeti"
        , "nose_exclude"
        ]
      }

     , entry_points =
       { 'nose.plugins':
         [ 'nose_focus = nose_focus.plugin:Plugin'
         ]
       }

    # metadata for upload to PyPI
    , url = "http://nose_focus.readthedocs.org"
    , author = "Stephen Moore"
    , author_email = "stephen@delfick.com"
    , description = "Decorator and plugin to make nose focus on specific tests"
    , license = "WTFPL"
    , keywords = "nose tests focus"
    )

