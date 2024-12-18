#!/usr/bin/python3

import pandas as pd
import sys
import argparse
import glob
import numpy as np
#----------------------------------------------------------------#
parser = argparse.ArgumentParser(description='Code Usage')
parser.add_argument('1', metavar='<Path>', help='Set file path')
args = parser.parse_args()
#----------------------------------------------------------------#
Files = glob.glob(f'{sys.argv[1]}/*flt*xlsx')
Files.sort()
#----------------------------------------------------------------#
MERGE = []

for File in Files:
    Sample = File.replace(f'{sys.argv[1]}' + '/', '')
    Sample = Sample.split('.')[0]

    Data = pd.read_excel(File,
                        index=False)
    Data = Data[pd.notna(Data.iloc[:, 0]) & ((Data.iloc[:, 1] == 'DEL') | (Data.iloc[:, 1] == 'DUP'))]
    Data.insert(0, 'Sample', Sample)
    MERGE.append(Data)

Merge_data = pd.concat(MERGE, axis=0)
Merge_data = Merge_data.sort_values(['Gene1','Gene2'])

Merge_data.to_excel('BPDCN.SV.mgd.xlsx',
                    index=False,
                    sheet_name='DEL & DUP')