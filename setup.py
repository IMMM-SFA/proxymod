import sys


try:
    from setuptools import setup, find_packages
except ImportError:
    raise('Missing Package: proxymod requires setuptools to install. Please install setuptools and retry.')


def get_requirements():
    with open('requirements.txt') as f:
        return f.read().split()


setup(
    name='proxymod',
    version='v0.0.1',
    packages=find_packages(),
    url='https://github.com/IMMM-SFA/proxymod',
    license='GNU V2',
    author='Chris R. Vernon',
    author_email='chris.vernon@pnnl.gov',
    description='A lightweight Python package to simulate model interactions',
    install_requires=get_requirements()
)
