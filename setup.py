import os
import sys
from setuptools import setup, find_packages
try:
    requirements = open('requirements.txt').read().strip().split('\n')
except:
    requirements = []

setup(
    name = 'tt',
    version = '0.1.0',
    packages = find_packages(),
    install_requires = requirements,
    dependency_links = ['https://github.com/PyBossa/pybossa-client/zipball/master#egg=pybossa_client'],
    # metadata for upload to PyPI
    author = 'LSD',
    # TODO: change
    author_email = '',
    description = 'Transcription application using pybossa.',
    long_description = '''.
    ''',
    license = 'MIT',
    url = '',
    download_url = '',
    include_package_data = True,
    classifiers = [
        'Development Status :: ',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points = '''
    '''
)
