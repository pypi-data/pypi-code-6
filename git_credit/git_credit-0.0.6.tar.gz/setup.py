"""git_credit installer."""


from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    """Shim in pytest to be able to use it with setup.py test."""

    def finalize_options(self):
        """Stolen from http://pytest.org/latest/goodpractises.html."""

        TestCommand.finalize_options(self)
        self.test_args = ["-v", "-rf", "--cov", "git_credit", "--cov-report",
                          "term-missing", "test"]
        self.test_suite = True

    def run_tests(self):
        """Also shamelessly stolen."""

        # have to import here, outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        raise SystemExit(errno)


setup(
    name="git_credit",
    version="0.0.6",
    author="Adam Talsma",
    author_email="adam@talsma.ca",
    packages=["git_credit"],
    scripts=["bin/git_credit"],
    url="https://github.com/a-tal/git_credit",
    description="A pretty way to show committer stats for git repos",
    long_description="Uses git log to display committer stats for git repos",
    download_url="https://github.com/a-tal/git_credit",
    install_requires=["bladerunner"],
    tests_require=["mock", "pytest", "pytest-cov", "coverage"],
    cmdclass={"test": PyTest},
    license="BSD",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
    ],
)
