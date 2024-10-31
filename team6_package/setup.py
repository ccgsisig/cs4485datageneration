from setuptools import setup, find_packages

setup(
    name='team6_package',
    version='0.1.4',
    description='Generate CSV data from a JSON schema.',
    author='Team_6',
    packages=find_packages(),
    install_requires=['faker'],
)