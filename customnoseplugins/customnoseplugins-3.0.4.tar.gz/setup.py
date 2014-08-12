try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='customnoseplugins',
    version="3.0.4",
    description = 'test plan plugins for the nose testing framework',
    author = 'bao hongbin',
    author_email = 'hongbin.bao@gmail.com',
    license = 'MIT',
    long_description = """\

Extra plugins for the nose testing framework to load test case from a plan file and specify the execute order in test suite\n

usage:\n
>>> nosetests --with-plan-loader --plan-file PATH_OF_PLAN_FILE --loop 10\n
>>> nosetests --with-plan-loader --plan-file PATH_OF_PLAN_FILE --loop 10 --timeout 180\n

plan file content:\n
[tests]\n
packagename.modulename.classname.testcasename1 = 3\n
packagename.modulename.classname.testcasename2 = 5\n


1: allow to custom a test plan file. the plan file can define the test cases name list  and the executed  loop count in one loop.\n All tests will be executed from top to end follow it's own loop count.\n
2: allow to define the test cycle number. the test will be executed cyclically until exceed the cycle number. default only\n executed 1 cycle.\n
3: set timeout limitation(seconds) for each test method

start from command-line:
    nosetests --with-plan-loader --plan-file PATH_OF_PLAN_FILE --loop 100
    nosetests --with-plan-loader --plan-file PATH_OF_PLAN_FILE --loop 100 --timeout 180

start programmly:\n
    >>> from customnoseplugins.planloader import PlanLoaderPlugin\n
    >>> nose.run(argv=['--with-plan-loader', '--plan-file', 'PATH_OF_PLAN_FILE', '--loop', 'INTEGER_NUMBER'], \naddplugins=[PlanLoaderPlugin()])\n
""",
    packages = ['customnoseplugins'],
    entry_points = {
        'nose.plugins': [
            'plan-loader = customnoseplugins.planloader:PlanLoaderPlugin',
            'file-output = customnoseplugins.fileoutput:FileOutputPlugin',
            ],
         },
)

