#!/usr/bin/python3

import pandas as pd
import sys
import glob
import argparse
#-----------------------------------------------------------------#
# parser = argparse.ArgumentParser(description='Code Usage')
# parser.add_argument('1', metavar='<File format>', help='Set File format')
# args = parser.parse_args()
#-----------------------------------------------------------------#
Files = glob.glob('bpdcn*xlsx')
Files.sort()
#-----------------------------------------------------------------#
Total = []
for sample in Files:
    Data = pd.read_excel(sample,
                         header=0)
    
    Flt = Data[Data['Result'] == 'T']
    Flt.insert(0, 'Sample', str(sample.split('.')[0]))
    Total.append(Flt)

Merged = pd.concat(Total)
Merged.to_excel(excel_writer='BPDCN.CNV.xlsx',
                sheet_name='CNV',
                header=0,
                index=False)