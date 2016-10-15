#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='file-dl',
    version='0.0.1.1',
    author='Animesh Kundu',
    description='File Download Accelerator written in pure python',
    author_email='anik.edu@gmail.com',
    packages=['accelerator'],
    scripts=[],
    url='https://github.com/animeshkundu/file-dl',
    license='LICENSE.txt',
    long_description=open('README.md').read(),
    install_requires=['futures==3.0.5'],
    entry_points={
        'console_scripts': ['file-dl = accelerator.__init__:main']
    },
)
