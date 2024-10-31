from setuptools import setup, find_packages

setup(
    name='team6_package',
    version='0.1.5',
    description='Generate CSV data from a JSON schema.',
    author='Team 6',
    packages=find_packages(),
    install_requires=['faker'],
    entry_points={
        'console_scripts': [
            'team6_package=team6_package.core:main'
        ]
    }
)