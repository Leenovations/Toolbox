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
def AllocateChr(): 
    parser = argparse.ArgumentParser(description='Pipeline Usage')
    parser.add_argument('1', metavar='<CpG>' ,help='CpG methylation file')
    parser.add_argument('2', metavar='<Bed>' ,help='Bed file')
    parser.add_argument('3', metavar='<Output>' ,help='Output file name')
    args = parser.parse_args()

    Merged_CpG = pd.read_csv(sys.argv[1], sep='\t', header=0, names=['Chromosome', 'Start', 'End', 'Strand', 'pvalue', 'qvalue', 'meth.diff'], low_memory=False)
    bed = pd.read_csv(sys.argv[2], sep='\t', header=0, names=['Chromosome', 'Start', 'End', 'Strand', 'GeneSymbol', 'NM', 'Region'], low_memory=False)

    pySubset = pr.PyRanges(bed)
    pyMerged = pr.PyRanges(Merged_CpG)

    Intersect = pySubset.join(pyMerged).df
    Intersect = Intersect.drop(['Strand_b'], axis=1)
    Intersect.rename(columns={'Start_b': 'Start_methylkit'}, inplace=True)
    Intersect.rename(columns={'End_b': 'End_methylkit'}, inplace=True)
    Intersect = Intersect.astype({'Chromosome': 'str', 'Start' : 'int', 'End' : 'int', 'GeneSymbol': 'str'})
    Intersect = Intersect.sort_values(by=['Chromosome', 'Start', 'End'])

    Intersect.to_csv(sys.argv[3], sep='\t', index=False)

if __name__=='__main__':
    AllocateChr()
#----------------------------------------------------------------------------------------#