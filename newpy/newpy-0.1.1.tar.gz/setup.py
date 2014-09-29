from setuptools import setup

setup(
        name="newpy",
        version="0.1.1",
        description="Quickly and easily create a new python project",
        url="https://bitbucket.org/edwardonsoftware/newpy",
        author="Edward",
        author_email="edwardprentice@gmail.com",
        keywords="tutorial new example skeleton",
        license="MIT",
        packages=["newpy"],
        zip_safe=False,
        include_package_data=True,
        data_files=[("resources", ["resources/Logger.py", "resources/simple_skeleton.py", "skeleton_with_logger.py"])],
        entry_points={
            'console_scripts': [
                'newpy=newpy:main',
            ],
        }

)
