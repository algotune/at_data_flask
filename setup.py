#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = []
setup_requirements = ['pytest-runner']

test_requirements = ['pytest>=3']

setup(
    author="Bin Yang",
    author_email='bin.yang@algotune.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="at_pypackage",
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='at_data_flask',
    name='at_data_flask',
    packages=find_packages(include=['at_data_flask', 'at_data_flask.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/algotune/at_data_flask',
    version='0.0.1',
    zip_safe=False,
)
