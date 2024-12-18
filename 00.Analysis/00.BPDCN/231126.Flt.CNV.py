#!/usr/bin/python3

import pandas as pd
import sys
import argparse
import glob
import os
#------------------------------------------------------------#
# parser = argparse.ArgumentParser(description='Code Usage')
# parser.add_argument('1', metavar='<Path>', help='Set Path')
# parser.add_argument('2', metavar='<Gene list>', help='Set Gene list file')
# args = parser.parse_args()
#------------------------------------------------------------#
Gene = pd.read_csv('/media/node02-HDD01/01.BPDCN_SV/00.Gene/Gene.txt',
                   sep='\t',
                   header=None)
Gene = Gene[0].tolist()
#------------------------------------------------------------#
Files = glob.glob('bpdcn_*_[0-9][0-9][0-9]')
Files.sort()
#------------------------------------------------------------#
for sample in Files:
    if os.path.isdir(sample + '_geneCNV'):
        pass
    else:
        command = f'mkdir {sample}_geneCNV'
        os.system(command)
# #------------------------------------------------------------#
for sample in Files:
    CNV = [f'/media/node02-HDD01/01.BPDCN_SV/02.GeneCNV/{sample}/gene.CNV/vs.batch.cases/' + item + '.' + sample + '.CNV.pdf' for item in Gene]
    for cnv in CNV:
        command = f'cp {cnv} /media/node02-HDD01/01.BPDCN_SV/02.GeneCNV/{sample}_geneCNV/'
        os.system(command)