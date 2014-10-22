from setuptools import setup, Extension

setup(
    name='openvcdiff',
    version='0.1',
    ext_modules=[Extension('openvcdiff',
        ['src/extension.cpp'],
        libraries=["vcdenc", "vcddec"],
    )],
    tests_require = ['nose >= 0.11'],
    test_suite = "nose.collector",
)
