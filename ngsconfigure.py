#!/usr/bin/python3
import sys
import os
import glob
import argparse
import pandas as pd
import numpy as np
import subprocess
#-----------------------------------------------------------------------------#
parser = argparse.ArgumentParser(description='Pipeline Usage')
args = parser.parse_args()
#-----------------------------------------------------------------------------#
command = 'pwd'
Dir = os.getcwd()
#-----------------------------------------------------------------------------#
command = f'cat SampleSheet.*.txt > SampleSheet.txt'
os.system(command)
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
with open('SampleSheet.txt', 'r') as samplesheet:
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
with open('batch.config', 'r') as batch:
    for line in batch:
        line = line.strip()
        splitted = line.split('=')
        Key = splitted[0]
        Value = splitted[1]
        BATCH[Key] = Value
#====================================================================================================================================#
BATCH['Tool_GATK'] = f"/media/src/DB/Tools/GATK_4.3/gatk-package-4.3.0.0-local.jar"
BATCH['Tool_Trimming'] = f"/media/src/DB/Tools/TrimGalore_0.6.10/trim_galore"
BATCH['Tool_Picard'] = f"/media/src/DB/Tools/picard/build/libs/picard.jar"
BATCH['Tool_Varscan2'] = f"/media/src/DB/Tools/VARSCAN_2.4.5/VarScan.v2.4.5.jar"
BATCH['Tool_snpeff'] = f"/media/src/DB/Tools/snpEff/snpEff.jar"
BATCH['Tool_MELT'] = f"/media/src/Tools/MELTv2.2.2/MELT.jar"
BATCH['Tool_Arriba'] = f"/media/src/DB/Tools/arriba_v2.4.0/arriba"
BATCH['Tool_Arriba_draw'] = f"/media/src/DB/Tools/arriba_v2.4.0/draw_fusions.R"
#====================================================================================================================================#
# BATCH['GTFidx'] = f"/media/src/DB/{BATCH['Ref.ver']}/01.GTF/NCBIp14.FASTA_NCBIp14.GTF"
# BATCH['GTF'] = f"/media/src/DB/{BATCH['Ref.ver']}/01.GTF/NCBI.{BATCH['Ref.ver']}.p14.gtf"
# BATCH['GTFidx'] = f"/media/src/DB/{BATCH['Ref.ver']}/01.GTF/UCSC.FASTA_GENCODEV48.GTF"
BATCH['GTFidx'] = f"/media/src/DB/{BATCH['Ref.ver']}/01.GTF/UCSC.FASTA_GENCODEV48.GTF"
BATCH['GTF'] = f"/media/src/DB/{BATCH['Ref.ver']}/01.GTF/gencode.v48.{BATCH['Ref.ver']}.gtf"
#====================================================================================================================================#
# BATCH['PON_WES'] = f"/media/src/DB/{BATCH['Ref.ver']}/03.PON/Mutect2_WES_pon_{BATCH['Ref.ver']}.vcf"
BATCH['Panel'] = f"/media/src/DB/{BATCH['Ref.ver']}/02.PANEL/Panel.{BATCH['Panel']}.{BATCH['Ref.ver']}.bed"
BATCH['BWA'] = f"/media/src/DB/{BATCH['Ref.ver']}/00.FASTA/Homo_sapiens_assembly{BATCH['Ref.ver'].split('g')[1]}.BWA2"
BATCH['FASTA'] = f"/media/src/DB/{BATCH['Ref.ver']}/00.FASTA/Homo_sapiens_assembly{BATCH['Ref.ver'].split('g')[1]}.fasta"
BATCH['dbSNP'] = f"/media/src/DB/{BATCH['Ref.ver']}/03.PON/Homo_sapiens_assembly{BATCH['Ref.ver'].split('g')[1]}.dbsnp138.vcf"
BATCH['dbINDEL'] = f"/media/src/DB/{BATCH['Ref.ver']}/03.PON/Homo_sapiens_assembly{BATCH['Ref.ver'].split('g')[1]}.known_indels.vcf"
BATCH['Mills'] = f"/media/src/DB/{BATCH['Ref.ver']}/03.PON/Mills_and_1000G_gold_standard.indels.{BATCH['Ref.ver']}.sites.vcf"
BATCH['gnomAD'] = f"/media/src/DB/{BATCH['Ref.ver']}/03.PON/af-only-gnomad.{BATCH['Ref.ver']}.vcf"
BATCH['PON'] = f"/media/src/DB/{BATCH['Ref.ver']}/03.PON/Mutect2_WGS_pon_{BATCH['Ref.ver']}.vcf"
BATCH['ExAC'] = f"/media/src/DB/{BATCH['Ref.ver']}/03.PON/small_exac_common_3.{BATCH['Ref.ver']}.vcf"
#====================================================================================================================================#
BATCH['Arriba_blacklist'] = f"/media/src/DB/ToolDB/Arriba/blacklist_{BATCH['Ref.ver']}_hs37d5_GRCh37_v2.4.0.tsv.gz"
BATCH['Arriba_knownDB'] = f"/media/src/DB/ToolDB/Arriba/known_fusions_{BATCH['Ref.ver']}_hs37d5_GRCh37_v2.4.0.tsv.gz"
BATCH['Arriba_proteinDomains'] = f"/media/src/DB/ToolDB/Arriba/protein_domains_{BATCH['Ref.ver']}_hs37d5_GRCh37_v2.4.0.gff3"
BATCH['Arriba_cytobands'] = f"/media/src/DB/ToolDB/Arriba/cytobands_{BATCH['Ref.ver']}_hs37d5_GRCh37_v2.4.0.tsv"
BATCH['Annovar'] = f"/media/src/DB/ToolDB/Annovar"
#====================================================================================================================================#
BATCH['Bismark_Reference_human'] = f"/media/src/DB/{BATCH['Ref.ver']}/00.FASTA/GENCODE.{BATCH['Ref.ver']}.bismark"
BATCH['Bismark_Reference_lambda'] = f"/media/src/DB/Metagenome/Lambda"
#====================================================================================================================================#
if BATCH['Node'] == 'node01' and int(BATCH['CPU']) > 128:
    raise ValueError("\033[91mValueError: Total CPU is less than 128\033[0m")
elif BATCH['Node'] == 'node02' and int(BATCH['CPU']) > 128:
    raise ValueError("\033[91mValueError: Total CPU is less than 56\033[0m")
elif BATCH['Node'] == 'node03' and int(BATCH['CPU']) > 128:
    raise ValueError("\033[91mValueError: Total CPU is less than 56\033[0m")
elif BATCH['Node'] == 'node04' and int(BATCH['CPU']) > 56:
    raise ValueError("\033[91mValueError: Total CPU is less than 56\033[0m")
elif BATCH['Node'] == 'node05' and int(BATCH['CPU']) > 56:
    raise ValueError("\033[91mValueError: Total CPU is less than 56\033[0m")
elif BATCH['Node'] == 'node06' and int(BATCH['CPU']) > 32:
    raise ValueError("\033[91mValueError: Total CPU is less than 32\033[0m")
#-----------------------------------------------------------------------------#
# if BATCH['Node'] == 'node05':
#     Cpu = int(BATCH['CPU'])
#     Allocated_CPU = int(Cpu / Sample_Count)
#     if Allocated_CPU < 1:
#         raise ValueError("\033[91m" + "ValueError: Allocated CPU is less than 1" + "\033[0m")
#     CPU = [Allocated_CPU] * Sample_Count
#     if Sample_Count > 1 :
#         How_many = int(Cpu % Sample_Count) #분배를 1씩 해주는 경우 -> 용량에 따라 나누어야함
#         for idx in Sample_Size_Idx[:How_many]:
#             CPU[idx] += 1
# elif BATCH['Node'] != 'node05':
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
    Code = '/labmed/00.Code/Pipeline/PANSeq.py FASTQ'
elif BATCH['Run.type'] == 'WES':
    Code = '/labmed/00.Code/Pipeline/PANSeq.py FASTQ'
elif BATCH['Run.type'] == 'TARGET':
    Code = '/labmed/00.Code/Pipeline/PANSeq.py FASTQ'
elif BATCH['Run.type'] == 'WGBS':
    Code = '/labmed/00.Code/Pipeline/PANSeq.py FASTQ'
elif BATCH['Run.type'] == 'RNA':
    Code = '/labmed/00.Code/Pipeline/PANSeq.py FASTQ'
elif BATCH['Run.type'] == 'Gleevec':
    Code = '/labmed/00.Code/Pipeline/PANSeq.py FASTQ'
elif BATCH['Run.type'] == 'Varaser':
    Code = '/labmed/00.Code/Pipeline/PANSeq.py FASTQ'
# if BATCH['Run.type'] == 'WGS':
#     Code = '/labmed/00.Code/Pipeline/WGS.py FASTQ'
# elif BATCH['Run.type'] == 'WES':
#     Code = '/labmed/00.Code/Pipeline/WES.py FASTQ'
# elif BATCH['Run.type'] == 'TARGET':
#     Code = '/labmed/00.Code/Pipeline/TARGET.py FASTQ'
# elif BATCH['Run.type'] == 'WGBS':
#     Code = '/labmed/00.Code/Pipeline/WGBS.py FASTQ'
# elif BATCH['Run.type'] == 'RNA':
#     Code = '/labmed/00.Code/Pipeline/RNASeq.py FASTQ'
# elif BATCH['Run.type'] == 'Gleevec':
#     Code = '/labmed/00.Code/Pipeline/Imatinib.py FASTQ'
# elif BATCH['Run.type'] == 'Varaser':
#     Code = '/labmed/00.Code/Varaser/Varaser.RNA.v3.py'
#-----------------------------------------------------------------------------#
with open('SampleSheet.txt', 'r') as samplesheet:
    num = 0
    for line in samplesheet:
        line = line.strip()
        splitted = line.split('\t')
        Name = splitted[0]
        R1 = splitted[1]
        R2 = splitted[2]
        Cpu = CPU[num]
        BATCH['CPU'] = CPU[num]
        BATCH['Sample.Run'] = Name
        BATCH['Sample.Dir'] = Dir + '/' + Name
        BATCH['R1'] = R1
        BATCH['R2'] = R2
        BATCH['Batch.Sample.Count'] = Sample_Count
        BATCH['Batch.Sample.Name'] = Sample_Name
        BATCH['Batch.Sample.Dir'] = Sample_Dir
        if os.path.isfile('SampleSheet.control.txt'):
            BATCH['Class'] = Matched[Name][0]
            BATCH['Matched.Sample.Name'] = Matched[Name][1].split('/')[-1]
            BATCH['Matched.Sample.dir'] = Matched[Name][1]
            with open(f'{Name}/{Name}.batch.config', 'w') as note:
                note.write('#===================================================================================#' + '\n')
                for Key in BATCH.keys():
                    note.write(Key + '=' + str(BATCH[Key]) + '\n')
                    if Key == 'AllowMismatch' or Key == 'Bismark_Reference_lambda' or Key == 'R2' or Key == 'Batch.Sample.Dir' or Key == 'tDepth' or Key == 'IGV.Snapshot' or Key == 'FilterScoreMin' or Key == 'Matched.Sample.dir':
                        note.write('#===================================================================================#' + '\n')
        else:
            with open(f'{Name}/{Name}.batch.config', 'w') as note:
                note.write('#===================================================================================#' + '\n')
                for Key in BATCH.keys():
                    note.write(Key + '=' + str(BATCH[Key]) + '\n')
                    if Key == 'AllowMismatch' or Key == 'Bismark_Reference_lambda' or Key == 'R2' or Key == 'Batch.Sample.Dir' or Key == 'tDepth' or Key == 'IGV.Snapshot' or Key == 'FilterScoreMin':
                        note.write('#===================================================================================#' + '\n')

        if BATCH['Run.type'] == 'Varaser':
            with open(f'{Name}/03.Output/job.sh', 'w') as note:
                note.write("#!/bin/bash" + '\n'
                            + "#" + '\n'
                            + f"#SBATCH -J {BATCH['Run.type']}.{Name}" + '\n'
                            + f"#SBATCH -o Log.%j.out" + '\n'
                            + f"#SBATCH --time=UNLIMITED" + '\n'
                            + f"#SBATCH --nodelist={BATCH['Node']}" + '\n'
                            + f"#SBATCH -n {Cpu}" + '\n'
                            + '\n'
                            + f"python3 {Code} {Name}.STAR.sorted.bam {Name}.haplotype.prcd.vcf {Name} -T fastq -N {Cpu}")
        else:
            with open(f'{Name}/job.sh', 'w') as note:
                note.write("#!/bin/bash" + '\n'
                            + "#" + '\n'
                            + f"#SBATCH -J {BATCH['Run.type']}.{Name}" + '\n'
                            + f"#SBATCH -o Log.%j.out" + '\n'
                            + f"#SBATCH --time=UNLIMITED" + '\n'
                            + f"#SBATCH --nodelist={BATCH['Node']}" + '\n'
                            + f"#SBATCH -n {Cpu}" + '\n'
                            + '\n'
                            + f"python3 {Code}")
        num += 1
#-----------------------------------------------------------------------------#
if BATCH['Run.type'] == 'Varaser':
    with open('Total.Run.sh', 'w') as note:
        with open('SampleSheet.txt', 'r') as samp:
            Sample_Count = 0
            for line in samp:
                line = line.strip()
                splitted = line.split('\t')
                Name = str(splitted[0])
                note.write('cd ' + Dir + '/' + Name + '/03.Output' + '; ' + 'sbatch job.sh' + '\n')
else:
    with open('Total.Run.sh', 'w') as note:
        with open('SampleSheet.txt', 'r') as samp:
            Sample_Count = 0
            for line in samp:
                line = line.strip()
                splitted = line.split('\t')
                Name = str(splitted[0])
                note.write('cd ' + Dir + '/' + Name + '; ' + 'sbatch job.sh' + '\n')
#-----------------------------------------------------------------------------#
