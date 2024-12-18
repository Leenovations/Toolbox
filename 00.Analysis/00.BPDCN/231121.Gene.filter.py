#!/usr/bin/python3

import pandas as pd
import sys
import argparse
import glob
import os
#------------------------------------------------------------#
parser = argparse.ArgumentParser(description='Code Usage')
parser.add_argument('1', metavar='<Path>', help='Set Path')
args = parser.parse_args()
#------------------------------------------------------------#
Target_list = pd.read_csv('/media/node02-HDD01/01.BPDCN_SV/00.Gene/Gene.txt',
                   sep='\t',
                   header=None)
#------------------------------------------------------------#
Files = glob.glob(f'{sys.argv[1]}/*tsv')
Files = glob.glob(f'/media/node02-HDD01/01.BPDCN_SV/01.SV/00.Original/*tsv')
Files.sort()
#------------------------------------------------------------#
if os.path.isdir('01.Filtered'):
    pass
else:
    command = 'mkdir 01.Filtered'
    os.system(command)
#------------------------------------------------------------#
def Filter(sv):
    Name = sv.split('/')[-1]
    Name = Name.split('.')[0]
    Name = Name + '.structural.flt.DEL.results.xlsx'

    SV = pd.read_csv(sv,
                     sep='\t',
                     header='infer')
    
    SV_filtered = SV
    SV_filtered = SV_filtered[(SV_filtered['Type'] == 'DEL') & (SV_filtered['FILTER'] == 'PASS') | (SV_filtered['Type'] == 'DUP') & (SV_filtered['FILTER'] == 'PASS')]

    SV_filtered = SV_filtered.dropna(subset=['Genes.Involved'])

    Total = []
    for row in range(0, SV_filtered.shape[0]):
        Gene = SV_filtered.iloc[row, SV_filtered.columns.get_loc('Genes.Involved')]
        if ',' in Gene:
            splitted = Gene.split(',')
            for gene in splitted:
                A = SV_filtered.iloc[row, :]
                A = pd.DataFrame(A)
                A = A.transpose()
                A.insert(13, 'Target', gene)
                Total.append(A)
        else:
            continue

    Merged = pd.concat(Total)
    Merged_flt = Merged[Merged['Target'].isin(Target_list.iloc[:,0].tolist())]
    Merged_flt.insert(0, 'Result', '')
    Merged_flt.to_excel(f'01.Filtered/{Name}',
                    header='infer',
                    index=False)
    
list(map(Filter, Files))

