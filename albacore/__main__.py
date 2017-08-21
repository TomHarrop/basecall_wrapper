#!/usr/bin/env python3

import argparse
import datetime
import shutil
import snakemake
import subprocess


# FUNCTIONS
def generate_message(message_text):
    """Format messages with date and time"""
    now = datetime.datetime.now().strftime('%a %b %d %H:%M:%S %Y')
    print('[ %s ]: %s' % (now, message_text))


# GLOBALS
snakefile = 'config/Snakefile'

# check if virtualenv is active
while not shutil.which("read_fast5_basecaller.py"):
    virtualenv_file = "albacore_env/bin/activate_this.py"
    generate_message("Trying to activate virtualenv\n%s" % virtualenv_file)
    global_namespace = {
        "__file__": virtualenv_file,
        "__name__": "__main__",
    }
    with open(virtualenv_file, 'rb') as file:
        exec(compile(file.read(), virtualenv_file, 'exec'), global_namespace)

generate_message("Using virtualenv python3: %s" %
                 shutil.which("python3"))

# parse fasta file from command line
generate_message("Parsing files")
parser = argparse.ArgumentParser()
parser.add_argument(
            '-y',
            required=True,
            help='other_input',
            type=str,
            dest='other_input',
            action='append')
parser.add_argument(
            '-z',
            required=True,
            help='other_output',
            type=str,
            dest='other_output')
args = vars(parser.parse_args())
other_input = [x for x in args['other_input']]
other_output = args['other_output']
print("Input file(s): %s" % other_input)
print("Output folder: %s" % other_output)

#run the pipeline
print("args: %s" % args)
snakemake.snakemake(
    snakefile=snakefile,
    config=args,
    printdag=True)

# print the graph CURRENTLY NOT WORKING, NEED TO USE API TO GET DAG
# dot_out = open('config/dag.svg', 'wb', 0)
# dot_in = subprocess.Popen(
#     ['dot', '-Tsvg'],
#     stdin=subprocess.PIPE, stdout=dot_out).stdin
# dag_proc = subprocess.Popen(
#     ['snakemake', '--snakefile', snakefile, '--dag', ],
#     stdout=dot_in)
# dag_proc.communicate()
