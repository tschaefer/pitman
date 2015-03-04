# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='pitman',
    version='0.0.1',
    packages=['pitman'],
    author='Tobias Schäfer',
    author_email='pitman@blackox.org',
    url='https://github.com/tschaefer/pitman',
    description='Dig for your favored Podcast.',
    license='BSD',
    install_requires=['feedparser>=5.1.3', 'requests>=2.4.3', 'clint>=0.4.1'],
    entry_points={'console_scripts': ['pitman=pitman.pitman:main']}
)
