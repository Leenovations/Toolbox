#!/usr/bin/python3

import sys
import os
import glob
import pandas as pd
import numpy as np
import time
from datetime import datetime
import concurrent.futures
import pyranges as pr
import multiprocessing
from functools import reduce
import argparse
#----------------------------------------------------------------------------------------#
parser = argparse.ArgumentParser(description='Pipeline Usage')
parser.add_argument('1', metavar='<CpG>' ,help='CpG methylation file')
parser.add_argument('2', metavar='<Bed>' ,help='Bed file')
parser.add_argument('3', metavar='<Output>' ,help='Output file name')
parser.add_argument('4', metavar='<CPU>' ,help='Number of CPU')
args = parser.parse_args()
#----------------------------------------------------------------------------------------#
def Calculate():
    # Chromosome = ['chr' + str(number) for number in range(1,23)] + ['chrX', 'chrY']
    Chromosome = [str(number) for number in range(1,23)] + ['X', 'Y']
    Merged_CpG = pd.read_csv(sys.argv[1], sep='\t', header=None, names=['Chromosome', 'Start', 'End', 'Strand', 'pvalue', 'qvalue', 'meth.diff'])

    Data_list = []
    bed = pd.read_csv(sys.argv[2], sep='\t', header=None, names=['Chromosome', 'Start', 'End', 'Strand', 'GeneSymbol', 'NM', 'Region'])

    def AllocateChr(chromosome): 
        if chromosome in list(Merged_CpG['Chromosome'].drop_duplicates()) and chromosome in list(bed['Chromosome'].drop_duplicates()):
            MergeSubset = Merged_CpG[Merged_CpG.iloc[:, 0] == chromosome]
            Subset = bed[bed.iloc[:, 0] == chromosome]

            pySubset = pr.PyRanges(Subset)
            pyMerged = pr.PyRanges(MergeSubset)

            Intersect = pySubset.join(pyMerged).df
            # Intersect = Intersect.drop(['Start_b', 'End_b'], axis=1)
            # Intersect = Intersect.astype({'Chromosome': 'str', 'Start' : 'int', 'End' : 'int', 'Gene': 'str'}) 	
            # Intersect = round(Intersect.groupby(['Chromosome', 'Start', 'End', 'Gene']).mean(), 3)
            # Intersect = Intersect.fillna('NaN')
            # Data_list.append(Intersect)

    if __name__ == '__main__':
        num_threads = int(sys.argv[4])
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            executor.map(AllocateChr, Chromosome)

    # Data = pd.concat(Data_list, axis = 0)
    # Data = Data.sort_values(by=['Chromosome', 'Start','End'])
    # Data = Data.reset_index()
    # Data.to_csv(sys.argv[3], sep='\t', index=False)

Calculate()