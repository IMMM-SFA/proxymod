import re
from setuptools import setup, find_packages


def readme():
    """Return the contents of the project README file."""

    with open('README.md') as f:
        return f.read()


version = re.search(r"__version__ = ['\"]([^'\"]*)['\"]", open('proxymod/__init__.py').read(), re.M).group(1)

setup(
    name='proxymod',
    version=version,
    packages=find_packages(),
    url='https://github.com/IMMM-SFA/proxymod',
    license='BSD-2-Clause',
    author='Chris R. Vernon',
    author_email='chris.vernon@pnnl.gov',
    description='A lightweight Python package to simulate model interactions',
    long_description=readme(),
    long_description_content_type="text/markdown",
    python_requires='>=3.8.*, <4',
    include_package_data=True,
    install_requires=[
        "configobj>=5.0.6",

    ],
    extras_require={
        'dev': [
        ]
    }
)
