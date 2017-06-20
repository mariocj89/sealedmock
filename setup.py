#!/usr/bin/env python
from setuptools import setup

exec(open('sealedmock/_version.py').read())

def readme():
    with open('README.rst') as f:
        return f.read()

import sys

if sys.version_info >= (3,0):
    install_requires = []
else:
    install_requires = ['mock']


setup(
    name='sealedmock',
    packages=['sealedmock'],
    version=__version__,
    description='Mocks that whitelist its interface',
    long_description=readme(),
    author='Mario Corchero',
    author_email='mariocj89@gmail.com',
    url='https://github.com/Mariocj89/sealedmock',
    keywords=['mock', 'testing', 'unittest', 'integration', 'whitelist'],
    license='MIT',
    use_2to3=True,
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
    ],
)
