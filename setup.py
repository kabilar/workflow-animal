#!/usr/bin/env python
from setuptools import setup, find_packages
from os import path
import sys

here = path.abspath(path.dirname(__file__))

long_description = """"
# Workflow for lab, animal, and session management

Build a workflow for lab management and animal metadata using DataJoint Elements
+ [elements-lab](https://github.com/datajoint/element-lab)
+ [elements-animal](https://github.com/datajoint/element-animal)
+ [elements-session](https://github.com/datajoint/element-session)
"""

with open(path.join(here, 'requirements.txt')) as f:
    requirements = f.read().splitlines()

setup(
    name='workflow-session',
    version='0.0.1',
    description="DataJoint Elements for Lab, Animal and Session Management",
    long_description=long_description,
    author='DataJoint',
    author_email='info@vathes.com',
    license='MIT',
    url='https://github.com/datajoint/workflow-session',
    keywords='neuroscience lab-management animal-management session-management datajoint',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=requirements,
)
