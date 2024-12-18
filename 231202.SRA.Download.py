#!/usr/bin/python3


import sys
import argparse
import glob
import time
import subprocess
import os
#-------------------------------------------------------------------------#
parser = argparse.ArgumentParser(description='Code Usage')
parser.add_argument('1', metavar='<Tool>', help='Select download tool')
parser.add_argument('2', metavar='<node>', help='Select node')
parser.add_argument('3', metavar='<Max>', help='Set Max CPU or None')
parser.add_argument('4', metavar='<SRA num>', nargs='+', help='Set SRA number')
args=parser.parse_args()
#-------------------------------------------------------------------------#
if os.path.isdir('00.RawData'):
    pass
else:
    command = 'mkdir 00.RawData'
    os.system(command)
#-------------------------------------------------------------------------#
if os.path.isdir('01.Finish'):
    pass
else:
    command = 'mkdir 01.Finish'
    os.system(command)
#-------------------------------------------------------------------------#
SRA_list = sys.argv[4:]
Sample_count = len(SRA_list)
#-------------------------------------------------------------------------#
def CPU_MAX():
    MAX_CPU = int(sys.argv[3])
    Allocated_CPU = 0

    if sys.argv[1] == 'fasterq-dump' :
        for sra in SRA_list:
            Allocated_CPU += 2

            command = f'mkdir -p 00.RawData/{sra}'
            os.system(command)

            with open(f'00.RawData/{sra}/job.sh', 'w') as note:
                note.write('#!/bin/bash' + '\n' + '#' + '\n' + \
                            '#SBATCH -J fasterq_dump' + '\n' + \
                            f'#SBATCH -o 00.RawData/{sra}/Log.%j.out' + '\n' + \
                            '#SBATCH --time=UNLIMITED' + '\n' + \
                            f'#SBATCH --nodelist={sys.argv[2]}' + '\n' + \
                            '#SBATCH -n 2' + '\n' + '\n' + \
                            f'fasterq-dump -S -t 00.RawData/{sra}/TEMP/ -e 8 -m 5000MB -O ../ {sra}' + '\n' + \
                            f'echo {sra} Raw data download is finished.\nPlease check log file. > 01.Finish/{sra}.txt')
            
            command = f'sbatch 00.RawData/{sra}/job.sh'
            os.system(command)

            if Allocated_CPU + 2 > MAX_CPU:
                break

        time.sleep(3600)

        Scheduled_SRA = SRA_list[int(MAX_CPU/2) : ]

        while True:
            Finished_SRA = os.listdir('01.Finish/')
            if len(Scheduled_SRA) != 0:
                for index in range(0, len(Finished_SRA)):
                    command = f'mkdir -p 00.RawData/{Scheduled_SRA[index]}'
                    os.system(command)

                    with open(f'00.RawData/{Scheduled_SRA[index]}/job.sh', 'w') as note:
                        note.write('#!/bin/bash' + '\n' + '#' + '\n' + \
                                    '#SBATCH -J fasterq_dump' + '\n' + \
                                    f'#SBATCH -o 00.RawData/{Scheduled_SRA[index]}/Log.%j.out' + '\n' + \
                                    '#SBATCH --time=UNLIMITED' + '\n' + \
                                    f'#SBATCH --nodelist={sys.argv[2]}' + '\n' + \
                                    '#SBATCH -n 2' + '\n' + '\n' + \
                                    f'fasterq-dump -S -t 00.RawData/{Scheduled_SRA[index]}/TEMP/ -e 8 -m 5000MB -O ../ {Scheduled_SRA[index]}' + '\n' + \
                                    f'echo {Scheduled_SRA[index]} Raw data download is finished.\nPlease check log file. > 01.Finish/{Scheduled_SRA[index]}.txt')

                    command = f'sbatch 00.RawData/{Scheduled_SRA[index]}/job.sh'
                    os.system(command)

                for index in range(0, len(Finished_SRA)):
                    Scheduled_SRA.pop(index)
                    os.remove('01.Finish/' + Finished_SRA[index])

                time.sleep(3600)
            else:
                break

    elif sys.argv[1] == 'fastq-dump' :
        for sra in SRA_list:
            Allocated_CPU += 2

            command = f'mkdir -p 00.RawData/{sra}'
            os.system(command)

            with open(f'00.RawData/{sra}/job.sh', 'w') as note:
                note.write('#!/bin/bash' + '\n' + '#' + '\n' + \
                            '#SBATCH -J fasterq_dump' + '\n' + \
                            f'#SBATCH -o 00.RawData/{sra}/Log.%j.out' + '\n' + \
                            '#SBATCH --time=UNLIMITED' + '\n' + \
                            f'#SBATCH --nodelist={sys.argv[2]}' + '\n' + \
                            '#SBATCH -n 2' + '\n' + '\n' + \
                            f'fastq-dump -S -t 00.RawData/{sra}/TEMP/ -e 8 -m 5000MB -O ../ {sra}' + '\n' + \
                            f'echo {sra} Raw data download is finished.\nPlease check log file. > 01.Finish/{sra}.txt')
            
            command = f'sbatch 00.RawData/{sra}/job.sh'
            os.system(command)

            if Allocated_CPU + 2 > MAX_CPU:
                break

        time.sleep(3600)

        Scheduled_SRA = SRA_list[int(MAX_CPU/2) : ]

        while True:
            Finished_SRA = os.listdir('01.Finish/')
            if len(Scheduled_SRA) != 0:
                for index in range(0, len(Finished_SRA)):
                    command = f'mkdir -p 00.RawData/{Scheduled_SRA[index]}'
                    os.system(command)

                    with open(f'00.RawData/{Scheduled_SRA[index]}/job.sh', 'w') as note:
                        note.write('#!/bin/bash' + '\n' + '#' + '\n' + \
                                    '#SBATCH -J fasterq_dump' + '\n' + \
                                    f'#SBATCH -o 00.RawData/{Scheduled_SRA[index]}/Log.%j.out' + '\n' + \
                                    '#SBATCH --time=UNLIMITED' + '\n' + \
                                    f'#SBATCH --nodelist={sys.argv[2]}' + '\n' + \
                                    '#SBATCH -n 2' + '\n' + '\n' + \
                                    f'fasterq-dump -S -t 00.RawData/{Scheduled_SRA[index]}/TEMP/ -e 8 -m 5000MB -O ../ {Scheduled_SRA[index]}' + '\n' + \
                                    f'echo {Scheduled_SRA[index]} Raw data download is finished.\nPlease check log file. > 01.Finish/{Scheduled_SRA[index]}.txt')

                    command = f'sbatch 00.RawData/{Scheduled_SRA[index]}/job.sh'
                    os.system(command)

                for index in range(0, len(Finished_SRA)):
                    Scheduled_SRA.pop(index)
                    os.remove('01.Finish/' + Finished_SRA[index])

                time.sleep(3600)
            else:
                break

def CPU_free():
    if sys.argv[1] == 'fasterq-dump':
        for sra in SRA_list:
            command = f'mkdir -p 00.RawData/{sra}'
            os.system(command)

            with open(f'00.RawData/{sra}/job.sh', 'w') as note:
                note.write('#!/bin/bash' + '\n' + '#' + '\n' + \
                            '#SBATCH -J fasterq_dump' + '\n' + \
                            '#SBATCH -o Log.%j.out' + '\n' + \
                            '#SBATCH --time=UNLIMITED' + '\n' + \
                            f'#SBATCH --nodelist={sys.argv[2]}' + '\n' + \
                            '#SBATCH -n 2' + '\n' + '\n' + \
                            f'fasterq-dump -S -t TEMP/ -e 8 -m 5000MB -O ../ {sra}')

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
                            '#SBATCH -J fastq_dump' + '\n' + \
                            '#SBATCH -o Log.%j.out' + '\n' + \
                            '#SBATCH --time=UNLIMITED' + '\n' + \
                            f'#SBATCH --nodelist={sys.argv[2]}' + '\n' + \
                            '#SBATCH -n 2' + '\n' + '\n' + \
                            f'fastq-dump --split-files -gzip --outdir ../ {sra}')

        with open('Total.Run.sh', 'w') as note:
            for sra in SRA_list:
                Path = os.getcwd()
                note.write(f'cd {Path}/00.RawData/{sra}; sbatch job.sh' + '\n')

if sys.argv[3] != 'None':
    CPU_MAX()
elif sys.argv[3] == 'None':
    CPU_free()