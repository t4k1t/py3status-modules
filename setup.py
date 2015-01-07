#!/usr/bin/python3

""" Setup script for py3status-modules. """
from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="py3status-modules",

    version='0.3.0',

    description="Collection of modules for py3status",

    long_description=long_description,

    # The project URL.
    url='https://www.github.com/tablet-mode/py3status-modules',

    # Author details
    author='Tablet Mode',
    author_email='tablet-mode@monochromatic.cc',

    # Choose your license
    license='GPLv3',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GPLv3 License',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Desktop Environment',
    ],

    keywords=['py3status', 'i3'],

    packages=find_packages(exclude=['docs', 'tests*']),

    # List run-time dependencies here. These will be installed by pip when your
    # project is installed.
    install_requires=[],

    # If there are data files included in your packages that need to be
    # installed, specify them here. If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={},

    data_files=[],

    entry_points={
    },
)
