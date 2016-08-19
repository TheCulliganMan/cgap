
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='cgap_v2',
    version='0.0.1',
    description='cgap_v2 package for Python-Guide.org',
    long_description=readme,
    author='Ryan Culligan',
    author_email='rrculligan@gmail.com',
    url='https://github.com/TheCulliganMan/cgap_v2',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
