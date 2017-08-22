#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pip
from setuptools import setup
from setuptools.command.install import install
from setuptools import find_packages

mac_url = ('https://mirror.oxfordnanoportal.com/software/analysis/'
           'ont_albacore-1.2.6-cp36-cp36m-macosx_10_11_x86_64.whl')
linux_url = ('https://mirror.oxfordnanoportal.com/software/analysis/'
             'ont_albacore-1.2.6-cp35-cp35m-manylinux1_x86_64.whl')

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        pip.main(['install', mac_url])

setup(
    cmdclass={'install': PostInstallCommand},
    name='basecall_wrapper',
    version='0.0.1',
    description='Tom\'s wrapper for ONT albacore',
    url='https://github.com/TomHarrop/basecall_wrapper',
    author='Tom Harrop',
    author_email='twharrop@gmail.com',
    license='GPL-3',
    packages=find_packages(),
    install_requires=[
        'snakemake>=4.0.0'
    ],
    zip_safe=False)
