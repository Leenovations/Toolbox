#!/usr/bin/python3

import argparse
import pandas as pd
import sys
import numpy as np
import concurrent.futures
#-----------------------------------------------------------------#
parser = argparse.ArgumentParser(description="Code Usage")
parser.add_argument("1", metavar="<window size>", help='Set window size')
parser.add_argument("2", metavar="<CPU>", help='Set CPU number')
args=parser.parse_args()
#-----------------------------------------------------------------#
Chromosome = pd.read_csv('/media/src/hg19/00.RNA/Index/chrNameLength.txt',
                         sep='\t',
                         header=None,
                         names = ['Chr','Length'])

Chromosome = Chromosome.iloc[:25,]
Chromosome = Chromosome.drop(22) #MT chromosome
#-----------------------------------------------------------------#
CHR = dict(zip(Chromosome.iloc[:,0], Chromosome.iloc[:,1]))
#-----------------------------------------------------------------#
RANGE = []
def MakeBed(chromosome):
    Start = np.arange(1, int(CHR[chromosome]), int(sys.argv[1]))
    End = Start + int(sys.argv[1]) - 1
    End[-1] = int(CHR[chromosome])

    Start = list(Start)
    End = list(End)

    chromosome = pd.DataFrame({'Chromosome' : chromosome,
                        'Start' : Start,
                        'End' : End})
    RANGE.append(chromosome)
    
if __name__ == '__main__':
    num_threads = int(sys.argv[2])
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(MakeBed, list(CHR.keys()))
#-----------------------------------------------------------------#
Data = pd.concat(RANGE)
Data = Data.sort_values(by=['Chromosome','Start','End'])
Data.to_csv(f'/media/src/hg19/01.Methylation/00.Bed/{sys.argv[1]}bp.bed',
            sep='\t',
            index=False,
            header=None)
#-----------------------------------------------------------------#