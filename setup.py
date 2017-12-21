# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='exp-sampler',
    version='0.1.0',
    description='Generic experiments sampler',
    long_description=readme,
    author='Dor Cohen',
    author_email='dorcoh@gmail.com',
    url='https://github.com/dorcoh/expsampler',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

