#!/usr/bin/env python

"""Setup script for before_after."""

import setuptools

from before_after import __project__, __version__


README = open('README.rst').read()

setuptools.setup(
    name=__project__,
    version=__version__,

    description="before_after provides utilities for testing race conditions",
    url='https://github.com/c-oreills/before_after',
    download_url='https://github.com/c-oreills/before_after/tarball/{v}'.
        format(v=__version__),
    author="Christy O'Reilly",
    author_email='christy@oreills.co.uk',

    packages=setuptools.find_packages(),

    entry_points={'console_scripts': []},

    long_description=README,
    license='GPLv2',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
    ],
    keywords = ['testing', 'race conditions'],

    install_requires=['mock==1.0.1'],
)
