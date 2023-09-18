from setuptools import setup, find_packages

setup(
    name='dbdict',
    version='0.0.1',
    author='shashstormer',
    description='A dictionary-like interface for using databases',
    packages=find_packages(),
    install_requires=[
        'pymongo',
    ],
)
