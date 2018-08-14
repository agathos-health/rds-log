#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', 'rollbar>=0.13.18', 'boto3>=1.4.7',]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Agathos",
    author_email='info@agathos.io',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Watch RDS logs for a database and transfer to S3",
    entry_points={
        'console_scripts': [
            'rds_log=rds_log.cli:main',
        ],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='rds_log',
    name='rds_log',
    packages=find_packages(include=['rds_log']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/tmcdonnell87/rds_log',
    version='0.1.0',
    zip_safe=False,
)
