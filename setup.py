#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages

setup(
    name='basecall_wrapper',
    version='0.0.1',
    description='Tom\'s wrapper for ONT albacore',
    url='https://github.com/TomHarrop/basecall_wrapper',
    author='Tom Harrop',
    author_email='twharrop@gmail.com',
    license='GPL-3',
    packages=find_packages(),
    install_requires=[
        'snakemake>=4.0.0',
        'ont_albacore>=1.2.6'
    ],
    dependency_links=[
        'https://mirror.oxfordnanoportal.com/software/analysis/ont_albacore-1.2.6-cp35-cp35m-manylinux1_x86_64.whl'
    ],
    zip_safe=False)
