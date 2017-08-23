#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import platform
import pip
import shutil
from setuptools import setup
from setuptools.command.install import install
from setuptools import find_packages

# check if bbtools is installed
bbmap_error = ('BBMap reformat.sh was not detected.\n'
               'Make sure BBMap is installed and the scripts are\n'
               'available from $PATH.\n'
               'http://jgi.doe.gov/data-and-tools/bbtools/'
               'bb-tools-user-guide/bbmap-guide/')
if shutil.which('reformat.sh') is None:
    raise EnvironmentError(bbmap_error)

mac_url = ('https://mirror.oxfordnanoportal.com/software/analysis/'
           'ont_albacore-1.2.6-cp36-cp36m-macosx_10_11_x86_64.whl')
linux_url = ('https://mirror.oxfordnanoportal.com/software/analysis/'
             'ont_albacore-1.2.6-cp35-cp35m-manylinux1_x86_64.whl')

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        if platform == 'darwin':
            pip.main(['install', mac_url])
        elif platform.startswith('linux'):
            pip.main(['install', linux_url])

setup(
    name='basecall_wrapper',
    version='0.0.3',
    description='Tom\'s wrapper for ONT albacore',
    url='https://github.com/TomHarrop/basecall_wrapper',
    author='Tom Harrop',
    author_email='twharrop@gmail.com',
    license='GPL-3',
    packages=find_packages(),
    install_requires=[
        'snakemake>=4.0.0',
        'psutil>=5.2.2'
    ],
    cmdclass={'install': PostInstallCommand},
    entry_points={
        'console_scripts': [
            'basecall_wrapper = basecall_wrapper.__main__:main'
            ],
    },
    package_data={
        'basecall_wrapper': ['config/Snakefile'],
    },
    zip_safe=False)
