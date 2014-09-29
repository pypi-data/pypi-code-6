from setuptools import setup

setup(
        name="newpy",
        version="0.1.4",
        description="Quickly and easily create a new python project",
        url="https://bitbucket.org/edwardonsoftware/newpy",
        author="Edward",
        author_email="edwardprentice@gmail.com",
        keywords="tutorial new example skeleton",
        license="MIT",
        packages=["newpy"],
        zip_safe=False,
        data_files=[("resources", ["resources/Logger.py", "resources/simple_skeleton.py", "resources/skeleton_with_logger.py"])],
        include_package_data=True,
        entry_points={
            'console_scripts': [
                'newpy=newpy:main',
            ],
        },
        classifiers=[
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 3 - Alpha',

            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',

            'License :: OSI Approved :: MIT License',

            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
        ],
)
