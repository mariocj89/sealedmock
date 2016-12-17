#!/usr/bin/env python
from setuptools import setup
LONG_DESCRIPTION="Mocks that can be restricted to the specified interface"

try:
    # attempt to build a long description from README.md
    # run sudo apt-get install pandoc and pip install pypandoc first
    import pypandoc
    LONG_DESCRIPTION=pypandoc.convert('README.md', 'rst')
except (ImportError, RuntimeError, OSError):
    pass


setup(
    name='sealedmock',
    packages=['sealedmock'],
    version='0.1.0',
    description='Mocks that whitelist its interface',
    long_description=LONG_DESCRIPTION,
    author='Mario Corchero',
    author_email='mariocj89@gmail.com',
    url='https://github.com/Mariocj89/sealedmock',
    keywords=['mock', 'testing', 'unittest', 'integration', 'whitelist'],
    license='MIT',
    use_2to3=True,
    install_requires=['mock'],
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
