basecall_wrapper
================

Wraps ONT albacore to basecall and provide a single merged ``fastq.gz`` of output along with some stats.

Requirements
------------

* ``python3`` 3.5 or newer with ``pip``
* ``reformat.sh`` from the BBmap_ package

Installation
------------

``pip3 install git+git://github.com/tomharrop/basecall_wrapper.git``

.. _BBmap: http://jgi.doe.gov/data-and-tools/bbtools/bb-tools-user-guide/bbmap-guide/ 

Usage
-----

.. code::

    usage: basecall_wrapper [-h] --input RAW_DATA --outdir OUTDIR --flowcell
                            FLOWCELL --kit KIT [--threads THREADS]
                            [--memory MEMORY]

    optional arguments:
      -h, --help           show this help message and exit
      --input RAW_DATA     .tar.gz files containing raw Nanopore data folders
      --outdir OUTDIR      Output directory
      --flowcell FLOWCELL  Flowcell type, e.g. FLO-MIN106
      --kit KIT            Sequencing kit, e.g. SQK-RAD003
      --threads THREADS    Number of threads.
      --memory MEMORY      Memory limit.