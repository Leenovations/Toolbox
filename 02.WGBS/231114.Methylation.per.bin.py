#!/usr/bin/python3

import os
import glob
import pandas as pd
import argparse
import sys
import concurrent.futures
import pyranges as pr
#-------------------------------------------------------------------------------------#
parser = argparse.ArgumentParser(description="Code Usage")
parser.add_argument('1', metavar='<bed>', help='Select Bed file')
args=parser.parse_args()
#-------------------------------------------------------------------------------------#
if os.path.isdir('CpG/02.bin/'):
    pass
else:
    command = 'mkdir CpG/02.bin/'
    os.system(command)
#-------------------------------------------------------------------------------------#
File = glob.glob('CpG/01.Trim/*cov')
File.sort()
Sample = [cov.replace('CpG/01.Trim/', '') for cov in File]
#-------------------------------------------------------------------------------------#
Bed = sys.argv[1]
Size = Bed.split('/')[-1].split('.')[0]
Bed = pd.read_csv(Bed,
                  sep='\t',
                  names=['Chromosome', 'Start', 'End'])
#-------------------------------------------------------------------------------------#
def Meth(cov):
    Data = pd.read_csv(cov,
                       sep='\t',
                       header='infer')
    
    pyData = pr.PyRanges(Data)
    pyBed = pr.PyRanges(Bed)

    Intersect = pyBed.join(pyData).df
    Intersect = Intersect.drop(['Start_b', 'End_b'], axis=1)
    Intersect = Intersect.astype({'Chromosome': 'str', 'Start' : 'int', 'End' : 'int', Data.columns[3] :'float'})
    Intersect = round(Intersect.groupby(['Chromosome', 'Start', 'End']).mean(), 2)
    Intersect = Intersect.fillna('NaN')
    Intersect = Intersect.reset_index()

    Intersect.to_csv(f'CpG/02.bin/{Data.columns[3]}.{Size}.cov',
                     sep='\t',
                     index=False)

list(map(Meth, File))

# if __name__ == '__main__':
#     num_threads = 30
#     with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
#         executor.map(Meth, File)
#-------------------------------------------------------------------------------------#