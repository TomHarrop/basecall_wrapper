#!/usr/bin/env python3

import argparse
import datetime
import io
import os
import shutil
import subprocess
import sys

# make sure virtualenv is active or try to activate it
try:
    import snakemake
except ImportError:
    print("Missing snakemake, trying to find virtualenv")
    try:
        venv_path = [x for (x, y, z) in os.walk('.')
                     if 'activate_this.py' in z][0]
        virtualenv_file = os.path.join(venv_path, 'activate_this.py')
        print("Trying to activate virtualenv: %s"
              % virtualenv_file)
        global_namespace = {
            "__file__": virtualenv_file,
            "__name__": "__main__",
        }
        with open(virtualenv_file, 'rb') as file:
            exec(compile(file.read(), virtualenv_file, 'exec'),
                 global_namespace)
        import snakemake
    except:
        raise ImportError("Couldn't activate virtualenv")


# FUNCTIONS
def generate_message(message_text):
    """Format messages with date and time"""
    now = datetime.datetime.now().strftime('%a %b %d %H:%M:%S %Y')
    print('[ %s ]: %s' % (now, message_text))


def print_graph(snakefile, config, dag_file):
    # store old stdout
    stdout = sys.stdout
    # call snakemake api and capture output
    sys.stdout = io.StringIO()
    snakemake.snakemake(
        snakefile,
        config=config,
        dryrun=True,
        printdag=True)
    output = sys.stdout.getvalue()
    # restore sys.stdout
    sys.stdout = stdout
    # pipe the output to dot
    with open(dag_file, 'wb') as svg:
        dot_process = subprocess.Popen(
            ['dot', '-Tsvg'],
            stdin=subprocess.PIPE,
            stdout=svg)
        dot_process.communicate(input=output.encode())


# GLOBALS
snakefile = 'config/Snakefile'

# did the virtualenv work?
generate_message("Using virtualenv python3: %s" %
                 shutil.which("python3"))

# parse fasta file from command line
generate_message("Parsing files")
parser = argparse.ArgumentParser()
parser.add_argument(
            '--input',
            required=True,
            help='.tar.gz files containing raw Nanopore data folders',
            type=str,
            dest='raw_data',
            action='append')
parser.add_argument(
            '--outdir',
            required=True,
            help='Output directory',
            type=str,
            dest='outdir')
args = vars(parser.parse_args())
raw_data = [x for x in args['raw_data']]
outdir = args['outdir']
print("Input file(s): %s" % raw_data)
print("Output folder: %s" % outdir)

# set up logging
log_dir = os.path.join(outdir, 'logs')
args['log_dir'] = log_dir
if not os.path.isdir(log_dir):
    os.makedirs(log_dir)

# print before dag
print_graph(snakefile, args, os.path.join(log_dir, "before.svg"))

#run the pipeline
print("args: %s" % args)
snakemake.snakemake(
    snakefile=snakefile,
    config=args)

# print after dag
print_graph(snakefile, args, os.path.join(log_dir, "after.svg"))