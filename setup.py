"""
Created on Wednesday 8 July, 15:00:00 2020

@author: Mark Connelly

Install the EZ-mcserver tool.
"""
from setuptools import setup, find_packages

setup(
    name='EZ-mcserver',
    version='1.0.0',
    author='Mark Connelly',
    description='Tool to create and manage a MineCraft server.',
    licence='MIT',
    url='https://github.com/plasmatech8/EZ-mcserver',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['mcserver=mcserver.cli:mcserver']
    },
    package_data={
        '': ['*.json']
    },
    install_requires=[
        'click'
    ],
)
