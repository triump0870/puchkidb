# coding=utf-8
from setuptools import setup, find_packages
from codecs import open
import os


def read(fname):
    path = os.path.join(os.path.dirname(__file__), fname)
    return open(path, encoding='utf-8').read()


# This will set the version string to __version__
exec (read('puchkidb/version.py'))

setup(
    name="puchkidb",
    version=__version__,
    packages=find_packages(exclude=['docs', 'tests*']),

    # development metadata
    zip_safe=True,

    # metadata for upload to PyPI
    author="Rohan Roy",
    author_email="rohan@rohanroy.com",
    description="A NoSQL database for small projects",
    license="MIT",
    keywords="database nosql cli",
    url="https://github.com/triump0870/puchkidb",
    classifiers=[
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        'Natural Language :: English',
        "Topic :: Database",
        "Topic :: Database :: Database Engines/Servers",
        "Topic :: Utilities",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent"
    ],
    tests_require=['pytest-cov', 'pyyaml'],
    setup_requires=['pytest-runner'],
    install_requires=['docopt'],
    long_description=read('README.rst'),
    entry_points={
        'console_scripts': [
            'puchkidb=puchkidb.puchkidb_cli.cli:main',
        ],
    },
)
