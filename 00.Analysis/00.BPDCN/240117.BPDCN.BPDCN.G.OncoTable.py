#!/usr/bin/python3

import pandas as pd
import argparse
import os
import sys
#------------------------------------------------------------#
parser = argparse.ArgumentParser(description='Code Usage')
parser.add_argument('1', metavar='<xlsx>', help='Set excel file')
parser.add_argument('2', metavar='<Output>', help='Set output file name')
args = parser.parse_args()
#------------------------------------------------------------#
Onco_Info = pd.read_excel(sys.argv[1],
                          header=0,
                          engine='openpyxl',
                          sheet_name='Sheet 1')
#------------------------------------------------------------#
Filtered = Onco_Info[Onco_Info.iloc[:, Onco_Info.columns.get_loc('Canonical')] != 'Synonymous']
Filtered = pd.DataFrame(Filtered)
#------------------------------------------------------------#
Sample = sorted(list(set(Filtered.iloc[:, Filtered.columns.get_loc('Name')].tolist())))
Gene = sorted(list(set(Filtered.iloc[:, Filtered.columns.get_loc('Gene')].tolist())))
Sample_idx = [num for num in range(0, len(Sample) + 1)]
SAMPLE = dict(zip(Sample, Sample_idx))
#------------------------------------------------------------#
Oncoprint = pd.DataFrame(columns = Sample,
                         index = Gene)
#------------------------------------------------------------#
for row in range(0, Filtered.shape[0]):
    Gene = Filtered.iloc[row, Filtered.columns.get_loc('Gene')]
    Classification = Filtered.iloc[row, Filtered.columns.get_loc('Canonical')]
    Sample = Filtered.iloc[row, Filtered.columns.get_loc('Name')]

    Row_Pos = Oncoprint.index.get_loc(Gene)
    current_value = Oncoprint.iat[Row_Pos, SAMPLE[Sample]]
    
    if isinstance(current_value, str) and current_value.strip() != '':
        Oncoprint.iat[Row_Pos, SAMPLE[Sample]] = current_value + '; ' + Classification
    else:
        Oncoprint.iat[Row_Pos, SAMPLE[Sample]] = Classification
#------------------------------------------------------------#
Oncoprint.to_excel(sys.argv[2],
                   header='infer',
                   index=True)
#------------------------------------------------------------#