#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shutil
import sys
import pip
from setuptools import setup
from setuptools.command.install import install
from setuptools import find_packages

# post-install albacore
mac_url = ('https://mirror.oxfordnanoportal.com/software/analysis/'
           'ont_albacore-2.0.2-cp36-cp36m-macosx_10_11_x86_64.whl')
linux_py4_url = ('https://mirror.oxfordnanoportal.com/software/analysis/'
                 'ont_albacore-2.0.2-cp34-cp34m-manylinux1_x86_64.whl')
linux_py5_url = ('https://mirror.oxfordnanoportal.com/software/analysis/'
                 'ont_albacore-2.0.2-cp35-cp35m-manylinux1_x86_64.whl')
linux_py6_url = ('https://mirror.oxfordnanoportal.com/software/analysis/'
                 'ont_albacore-2.0.2-cp36-cp36m-manylinux1_x86_64.whl')

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        if sys.platform == 'darwin':
            pip.main(['install', mac_url])
        elif sys.platform.startswith('linux'):
            if sys.version_info.minor == 4:
                pip.main(['install', linux_py4_url])
            elif sys.version_info.minor == 5:
                pip.main(['install', linux_py5_url])
            elif sys.version_info.minor == 6:
                pip.main(['install', linux_py6_url])

# check if bbtools is installed
bbmap_error = ('BBMap reformat.sh was not detected. '
               'Make sure BBMap is installed and the scripts are '
               'available from $PATH.'
               '\nhttp://jgi.doe.gov/data-and-tools/bbtools/'
               'bb-tools-user-guide/bbmap-guide/')
if sys.platform == 'darwin':
    bbmap_error += ('\n'
                    'On macOS, BBMap can be installed with '
                    '`brew install bbtools`')
if shutil.which('reformat.sh') is None:
    raise EnvironmentError(bbmap_error)

# load README.rst
def readme():
    with open('README.rst') as file:
        return file.read()

# main setup script
setup(
    name='basecall_wrapper',
    version='0.0.11',
    description='Tom\'s wrapper for ONT albacore',
    long_description=readme(),
    url='https://github.com/TomHarrop/basecall_wrapper',
    author='Tom Harrop',
    author_email='twharrop@gmail.com',
    license='GPL-3',
    packages=find_packages(),
    install_requires=[
        'biopython>=1.70',
        'numpy>=1.13.1',
        'psutil>=5.2.2',
        'snakemake>=4.0.0'        
    ],
    cmdclass={'install': PostInstallCommand},
    entry_points={
        'console_scripts': [
            'basecall_wrapper = basecall_wrapper.__main__:main'
            ],
    },
    package_data={
        'basecall_wrapper': [
            'config/Snakefile',
            'README.rst'
        ],
    },
    zip_safe=False)
