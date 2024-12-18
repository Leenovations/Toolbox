#!/usr/bin/python3

import os
import pandas as pd
import argparse
import sys
import pyranges as pr
import glob
import concurrent.futures
#-------------------------------------------------------------------------------------#
parser = argparse.ArgumentParser(description='Code Usage')
parser.add_argument('1', metavar='<bed>', help='Select bed file for position annotation')
# parser.add_argument('2', metavar='<CPU>', help='Set CPU core number')
args = parser.parse_args()
#-------------------------------------------------------------------------------------#
if os.path.isdir('CpG/03.Annotated'):
    pass
else:
    os.makedirs('CpG/03.Annotated', exist_ok=False)
#-------------------------------------------------------------------------------------#
Coverage = glob.glob('CpG/02.bin/*cov')
#-------------------------------------------------------------------------------------#
Bed = pd.read_csv(sys.argv[1],
                  sep='\t',
                  names = ['Chromosome', 'Start', 'End', 'Gene', 'Region', 'Strand'])
#-------------------------------------------------------------------------------------#
def Annotation(cov):
    Data = pd.read_csv(cov,
                       sep='\t',
                       header='infer')
    
    pyData = pr.PyRanges(Data)
    pyBed = pr.PyRanges(Bed)

    Intersect = pyBed.join(pyData).df
    Intersect = Intersect.drop(['Start_b', 'End_b'], axis=1)
    Intersect = Intersect.astype({'Chromosome': 'str', 'Start' : 'int', 'End' : 'int', 'Gene' : 'str', 'Region' : 'str', 'Strand' : 'str' , Data.columns[3] :'float'})
    Intersect = round(Intersect.groupby(['Chromosome', 'Start', 'End', 'Gene', 'Region', 'Strand']).mean(), 2)
    Intersect = Intersect.reset_index()
    Intersect['Strand'] = Intersect['Strand'].replace('nan', '*')

    Intersect.to_csv(f'CpG/03.Annotation/{Data.columns[3]}.Anno.cov',
                    sep='\t',
                    index=False)
#-------------------------------------------------------------------------------------#
list(map(Annotation, Coverage))
# if __name__ == '__main__':
#     num_threads = int(sys.argv[2])
#     with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
#         executor.map(Annotation, Coverage)
#-------------------------------------------------------------------------------------#