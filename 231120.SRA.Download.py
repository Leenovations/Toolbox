#!/usr/bin/python3

import os
import sys
import argparse
#-------------------------------------------------------------------------#
parser = argparse.ArgumentParser(description='Code Usage')
parser.add_argument('1', metavar='<Tool>', help='Select download tool')
parser.add_argument('2', metavar='<node>', help='Select node')
parser.add_argument('3', metavar='<SRA num>', nargs='+', help='Set SRA number')
args=parser.parse_args()
#-------------------------------------------------------------------------#
if os.path.isdir('00.RawData'):
    pass
else:
    command = 'mkdir 00.RawData'
    os.system(command)
#-------------------------------------------------------------------------#
SRA_list = sys.argv[3:]
#-------------------------------------------------------------------------#
if sys.argv[1] == 'fasterq-dump':
    for sra in SRA_list:
        command = f'mkdir -p 00.RawData/{sra}'
        os.system(command)

        with open(f'00.RawData/{sra}/job.sh', 'w') as note:
            note.write('#!/bin/bash' + '\n' + '#' + '\n' + \
                        f'#SBATCH -J {sra}.fasterq_dump' + '\n' + \
                        '#SBATCH -o Log.%j.out' + '\n' + \
                        '#SBATCH --time=UNLIMITED' + '\n' + \
                        f'#SBATCH --nodelist={sys.argv[2]}' + '\n' + \
                        '#SBATCH -n 2' + '\n' + '\n' + \
                        f'/media/src/Tools/sratoolkit.3.1.1-ubuntu64/bin/fasterq-dump -S -t TEMP/ -e 2 -O ../ {sra}')

    with open('Total.Run.sh', 'w') as note:
        for sra in SRA_list:
            Path = os.getcwd()
            note.write(f'cd {Path}/00.RawData/{sra}; sbatch job.sh' + '\n')

elif sys.argv[1] == 'fastq-dump':
    for sra in SRA_list:
        command = f'mkdir -p 00.RawData/{sra}'
        os.system(command)

        with open(f'00.RawData/{sra}/job.sh', 'w') as note:
            note.write('#!/bin/bash' + '\n' + '#' + '\n' + \
                        f'#SBATCH -J {sra}.fastq_dump' + '\n' + \
                        '#SBATCH -o Log.%j.out' + '\n' + \
                        '#SBATCH --time=UNLIMITED' + '\n' + \
                        f'#SBATCH --nodelist={sys.argv[2]}' + '\n' + \
                        '#SBATCH -n 2' + '\n' + '\n' + \
                        f'/media/src/Tools/sratoolkit.3.1.1-ubuntu64/bin/fastq-dump --split-files -gzip --outdir ../ {sra}')

    with open('Total.Run.sh', 'w') as note:
        for sra in SRA_list:
            Path = os.getcwd()
            note.write(f'cd {Path}/00.RawData/{sra}; sbatch job.sh' + '\n')
