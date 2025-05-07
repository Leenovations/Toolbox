#!/usr/bin/python3
import sys
import os
import glob
import argparse
import pandas as pd
import numpy as np
#-----------------------------------------------------------------------------#
parser = argparse.ArgumentParser(description='Pipeline Usage')
args = parser.parse_args()
#-----------------------------------------------------------------------------#
command = 'pwd'
Dir = os.getcwd()
#-----------------------------------------------------------------------------#
if os.path.isfile('SampleSheet.control.txt'):
    Matched = {}
    with open('SampleSheet.case.txt', 'r') as case, open('SampleSheet.control.txt') as control:
        for a, b in zip(case, control):
            case_line = a.strip()
            case_splitted = case_line.split('\t')[0]
            
            control_line = b.strip()
            control_splitted = control_line.split('\t')[0]

            Matched[case_splitted] = ['case', Dir + '/' + control_splitted]
            Matched[control_splitted] = ['control', Dir + '/' + case_splitted]
#-----------------------------------------------------------------------------#
with open('BAMSampleSheet.txt', 'r') as samplesheet:
    Sample_Count = 0
    Sample_Dir = []
    Sample_Name = []
    Sample_Size = []
    for line in samplesheet:
        Sample_name = line.split('\t')[0]
        Sample_Name.append(Sample_name)
        Sample_size = line.split('\t')[3].replace(' MB', '')
        Sample_Size.append(float(Sample_size))
        Sample_Count += 1
        Sample_Dir.append(Dir + '/' + Sample_name + '/')
    Sample_Dir = ','.join(Sample_Dir)
    Sample_Name = ','.join(Sample_Name)

Sample_Size_Sorted = sorted(Sample_Size, reverse=True)
Sample_Size_Idx = []
for num in Sample_Size_Sorted:
    idx = Sample_Size.index(num)
    Sample_Size_Idx.append(idx)
    Sample_Size[idx] = 0
#-----------------------------------------------------------------------------#
BATCH = {}
with open('BAM.batch.config', 'r') as batch:
    for line in batch:
        line = line.strip()
        splitted = line.split('=')
        Key = splitted[0]
        Value = splitted[1]
        BATCH[Key] = Value
#-----------------------------------------------------------------------------#
if BATCH['Node'] == 'node01' and int(BATCH['CPU']) > 128:
    raise ValueError("\033[91mValueError: Total CPU is less than 128\033[0m")
elif BATCH['Node'] == 'node02' and int(BATCH['CPU']) > 56:
    raise ValueError("\033[91mValueError: Total CPU is less than 56\033[0m")
elif BATCH['Node'] == 'node03' and int(BATCH['CPU']) > 32:
    raise ValueError("\033[91mValueError: Total CPU is less than 32\033[0m")
elif BATCH['Node'] == 'node04' and int(BATCH['CPU']) > 56:
    raise ValueError("\033[91mValueError: Total CPU is less than 28\033[0m")
#-----------------------------------------------------------------------------#
if BATCH['Node'] == 'node04':
    Cpu = int(BATCH['CPU'])
    Allocated_CPU = int(Cpu / Sample_Count)
    if Allocated_CPU < 1:
        raise ValueError("\033[91m" + "ValueError: Allocated CPU is less than 1" + "\033[0m")
    CPU = [Allocated_CPU] * Sample_Count
    if Sample_Count > 1 :
        How_many = int(Cpu % Sample_Count) #분배를 1씩 해주는 경우 -> 용량에 따라 나누어야함
        for idx in Sample_Size_Idx[:How_many]:
            CPU[idx] += 1
elif BATCH['Node'] != 'node04':
    Cpu = int(BATCH['CPU'])
    Allocated_CPU = int(Cpu / Sample_Count)
    if Allocated_CPU < 2:
        raise ValueError("\033[91m" + "ValueError: Allocated CPU is less than 2" + "\033[0m")
    elif Allocated_CPU >= 2:
        if Allocated_CPU % 2 == 0:
            if int(Cpu % Sample_Count) < 2:
                CPU = [Allocated_CPU] * Sample_Count
            elif int(Cpu % Sample_Count) >= 2:
                CPU = [Allocated_CPU] * Sample_Count
                How_many = int((Cpu % Sample_Count) / 2) #분배를 2씩 해주는 경우 -> 용량에 따라 나누어야함
                for idx in Sample_Size_Idx[:How_many]:
                    CPU[idx] += 2
        elif Allocated_CPU % 2 == 1:
            CPU = [Allocated_CPU - 1] * Sample_Count
            Rest_CPU = Sample_Count + Cpu % Sample_Count
            How_many = int(Rest_CPU / 2) #분배를 2씩 해주는 경우 -> 용량에 따라 나누어야함
            for idx in Sample_Size_Idx[:How_many]:
                CPU[idx] += 2
#-----------------------------------------------------------------------------#
if BATCH['Run.type'] == 'WGS':
    Code = '/labmed/00.Code/Pipeline/WGS.py BAM'
    if os.path.isdir("Results"):
        pass
    else:
        command = "mkdir -p Results/"
        os.system(command)
elif BATCH['Run.type'] == 'WES':
    Code = '/labmed/00.Code/Pipeline/WES.py BAM'
    if os.path.isdir("Results"):
        pass
    else:
        command = "mkdir -p Results/"
        os.system(command)
elif BATCH['Run.type'] == 'WGBS':
    Code = '/labmed/00.Code/Pipeline/WGBS.py BAM'
    if os.path.isdir("Results"):
        pass
    else:
        command = "mkdir -p Results/"
        os.system(command)
elif BATCH['Run.type'] == 'RNA':
    Code = '/labmed/00.Code/Pipeline/RNASeq.py BAM'
    if os.path.isdir("Genecount"):
        pass
    else:
        command = "mkdir -p Genecount/"
        os.system(command)
elif BATCH['Run.type'] == 'TARGET':
    Code = '/labmed/00.Code/Pipeline/TARGET.py BAM'
    if os.path.isdir("Genecount"):
        pass
    else:
        command = "mkdir -p Genecount/"
        os.system(command)
elif BATCH['Run.type'] == 'Gleevec':
    Code = '/labmed/00.Code/Pipeline/Imatinib.py BAM'
    if os.path.isdir("Results"):
        pass
    else:
        command = "mkdir -p Results/"
        os.system(command)
elif BATCH['Run.type'] == 'Varaser':
    Code = f'/labmed/00.Code/Varaser/Varaser.RNA.v3.py'
    if os.path.isdir("Results"):
        pass
    else:
        command = "mkdir -p Results/"
        os.system(command)
#-----------------------------------------------------------------------------#
with open('BAMSampleSheet.txt', 'r') as samplesheet:
    num = 0
    for line in samplesheet:
        line = line.strip()
        splitted = line.split('\t')
        Name = splitted[0]
        BAM_file = splitted[1].split('/')[-1]
        Cpu = CPU[num]
        BATCH['CPU'] = CPU[num]
        BATCH['SampleCount'] = Sample_Count
        BATCH['Sample.Name'] = Sample_Name
        BATCH['Sample.Dir'] = Sample_Dir
        Free_Memory = int(os.popen("free -g | grep Mem | awk '{print $7}'").read().strip())
        Free_Memory = int(Free_Memory*0.5/Sample_Count)
        BATCH['Memory'] = Free_Memory
        if os.path.isfile('SampleSheet.control.txt'):
            BATCH['Class'] = Matched[Name][0]
            BATCH['Matched.Sample.Name'] = Matched[Name][1].split('/')[-1]
            BATCH['Matched.Sample.dir'] = Matched[Name][1]
            with open(f'{Name}/{Name}.batch.config', 'w') as note:
                for Key in BATCH.keys():
                    note.write(Key + '=' + str(BATCH[Key]) + '\n')
        else:
            with open(f'{Name}/{Name}.batch.config', 'w') as note:
                for Key in BATCH.keys():
                    note.write(Key + '=' + str(BATCH[Key]) + '\n')

        if BATCH['Run.type'] == 'Varaser':
            with open(f'{Name}/BAMjob.sh', 'w') as note:
                note.write("#!/bin/bash" + '\n'
                            + "#" + '\n'
                            + f"#SBATCH -J {BATCH['Run.type']}.{Name}" + '\n'
                            + f"#SBATCH -o Log.%j.out" + '\n'
                            # + f"#SBATCH -e Error.%j.out" + '\n'
                            + f"#SBATCH --time=UNLIMITED" + '\n'
                            + f"#SBATCH --nodelist={BATCH['Node']}" + '\n'
                            + f"#SBATCH -n {Cpu}" + '\n'
                            + '\n'
                            + f"python3 {Code} 03.Output/{Name}.sorted.bam 03.Output/{Name}.haplotype.prcd.vcf {Name} 03.Output -T fastq -N {Cpu}")
        else:
            with open(f'{Name}/BAMjob.sh', 'w') as note:
                note.write("#!/bin/bash" + '\n'
                            + "#" + '\n'
                            + f"#SBATCH -J {BATCH['Run.type']}.{Name}" + '\n'
                            + f"#SBATCH -o Log.%j.out" + '\n'
                            # + f"#SBATCH -e Error.%j.out" + '\n'
                            + f"#SBATCH --time=UNLIMITED" + '\n'
                            + f"#SBATCH --nodelist={BATCH['Node']}" + '\n'
                            + f"#SBATCH -n {Cpu}" + '\n'
                            + '\n'
                            + f'Memory=$(echo "$(free -g | grep Mem | awk \'{{print $7}}\') * 0.7 / {Sample_Count}" | bc)' + '\n'
                            + f"echo Memory=$Memory >> {Name}.batch.config" + '\n'                        
                            + f"python3 {Code}")
                            # + f"python3 {Code} /labmed/02.AML/03.RNA/{Name.replace('_Aligned', '')}/03.Output/{Name}.sortedByCoord.out.bam")
        num += 1
#-----------------------------------------------------------------------------#
with open('Total.Run.BAM.sh', 'w') as note:
    with open('BAMSampleSheet.txt', 'r') as samp:
        Sample_Count = 0
        for line in samp:
            line = line.strip()
            splitted = line.split('\t')
            Name = str(splitted[0])
            note.write('cd ' + Dir + '/' + Name + '; ' + 'sbatch BAMjob.sh' + '\n')
#-----------------------------------------------------------------------------#
