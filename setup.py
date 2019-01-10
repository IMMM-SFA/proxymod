
try:
    from setuptools import setup, find_packages
except ImportError:
    raise('Missing Package: proxymod requires "setuptools" to install. Install "setuptools" and retry.')


def get_requirements():
    with open('requirements.txt') as f:
        return f.read().split()


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='proxymod',
    version='0.1.0',
    packages=find_packages(),
    url='https://github.com/IMMM-SFA/proxymod',
    license='BSD 2-Clause',
    author='Chris R. Vernon',
    author_email='chris.vernon@pnnl.gov',
    description='A lightweight Python package to simulate model interactions',
    long_description=readme(),
    install_requires=get_requirements()
)
