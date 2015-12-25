#!/usr/bin/env python
from setuptools import setup, find_packages
from codecs import open
from os import path
from liqpay import __version__, __title__


here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='liqpay',
    version=__version__,
    description=__title__,
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='liqpay payment',
    packages=find_packages(),
    install_requires=['requests'],
)
