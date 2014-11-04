from setuptools import setup


reqs = ['boto>=2.34.0', 'pyyaml>=3.11']

setup(
    include_package_data=True,
    name='aws_ops',
    author="Chris Maxwell",
    author_email="foo@bar.com",
    version='0.0.2',
    description="Building special snowflakes consistently",
    packages=[
        "cloudcaster",
        "ec2cleanlc",
        "ec2cleanami",
        "ec2autoimage",
        "ec2createapp",
        "ec2nodefind",
        "ec2rotatehosts"
    ],
    scripts=[
        "cloudcaster/cloudcaster.py",
        "ec2cleanlc/ec2cleanlc.py",
        "ec2cleanami/ec2cleanami.py",
        "ec2autoimage/ec2autoimage.py",
        "ec2createapp/ec2createapp.py",
        "ec2nodefind/ec2nodefind.py",
        "ec2rotatehosts/ec2rotatehosts.py",
    ],
    entry_points={
        "console_scripts": [
            "cloudcaster = cloudcaster.cloudcaster:main",
            "ec2cleanlc = ec2cleanlc.ec2cleanlc:main",
            "ec2cleanami = ec2cleanami.ec2cleanami:main",
            "ec2autoimage = ec2autoimage.ec2autoimage:main",
            "ec2createapp = ec2createapp.ec2createapp:main",
            "ec2nodefind = ec2nodefind.ec2nodefind:main",
            "ec2rotatehosts = ec2rotatehosts.ec2rotatehosts:main",
        ]
    },
    url="https://github.com/WrathOfChris/ops",
    install_requires=reqs,
    license="BSD 2-Clause"
)
