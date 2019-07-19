#!/usr/bin/env python
from os.path import join

from setuptools import setup, find_packages


MODULE_NAME = 'app'
REPO_NAME = 'ports-adapters-sample'


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()


setup(
    name=MODULE_NAME,
    description=('A sample project that uses the ports and adapters'
                 ' architecture (or hexagonal architecture) for a micro'
                 ' service'),
    license=license,
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/LucasRGoes/{:s}'.format(REPO_NAME),
    author='Lucas Góes',
    author_email='lucas.rd.goes@gmail.com',
    packages=find_packages(exclude=('tests')),
    version=open(join(MODULE_NAME, 'VERSION')).read().strip(),
    install_requires=[],
    classifiers=['Programming Language :: Python :: 3.6']
)
