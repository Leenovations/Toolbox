#!/usr/bin/python3

import os
import sys
#-------------------------------------------------------------------------#
if os.path.isdir('00.RawData'):
    pass
else:
    command = 'mkdir 00.RawData'
    os.system(command)
#-------------------------------------------------------------------------#
SRA_list = sys.argv[2:]
#-------------------------------------------------------------------------#
for sra in SRA_list:
    command = f'mkdir -p 00.RawData/{sra}'
    os.system(command)
        
    command = f'mkdir -p 00.RawData/{sra}'
    os.system(command)

    with open(f'00.RawData/{sra}/job.sh', 'w') as note:
        note.write('#!/bin/bash' + '\n' + '#' + '\n' + \
                    '#SBATCH -J fastq_dump' + '\n' + \
                    '#SBATCH -o Log.%j.out' + '\n' + \
                    f'#SBATCH --nodelist={sys.argv[1]}' + '\n' + \
                    '#SBATCH -n 2' + '\n' + '\n' + \
                    f'fastq-dump --split-files -gzip --outdir ../ {sra}')

with open('Total.Run.sh', 'w') as note:
    for sra in SRA_list:
        Path = os.getcwd()
        note.write(f'cd {Path}/00.RawData/{sra}; sbatch job.sh' + '\n')