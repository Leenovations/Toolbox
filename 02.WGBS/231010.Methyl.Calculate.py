import sys
import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import datetime
import concurrent.futures
import pyranges as pr
import multiprocessing
from functools import reduce

def Calculate():
    Chromosome = ['chr' + str(number) for number in range(1,23)] + ['chrX', 'chrY']

    Bed_list = ['/media/src/hg19/01.Methylation/00.Bed/NCBI.RefSeq.Selected.hg19.Total.bed']

    Merged_CpG = pd.read_csv(f'/labmed/06.AML/Result/04.Normal/231012.150bp.Normalized.txt', sep='\t', header='infer')

    for bed in Bed_list:
        Prefix = bed.split('/')[-1]
        Prefix = Prefix.split('.bed')[0]
        Data_list = []
        bed = pd.read_csv(bed, sep='\t', header=None)

        def AllocateChr(chromosome): 
            if chromosome in list(Merged_CpG['Chromosome'].drop_duplicates()) and chromosome in list(bed[0].drop_duplicates()):
                MergeSubset = Merged_CpG[Merged_CpG.iloc[:, 0] == chromosome]
                Subset = bed[bed.iloc[:, 0] == chromosome]
                Subset.columns = ['Chromosome','Start','End', 'GeneSymbol', 'Type', 'Strand']
                pySubset = pr.PyRanges(Subset)
                pyMerged = pr.PyRanges(MergeSubset)

                Intersect = pySubset.join(pyMerged).df
                Intersect = Intersect.drop(['Start_b', 'End_b'], axis=1)
                Intersect = Intersect.astype({'Chromosome': 'str', 'Start' : 'int', 'End' : 'int', 'GeneSymbol' : 'str', 'Type' : 'str', 'Strand' : 'str'})
                Intersect = round(Intersect.groupby(['Chromosome', 'Start', 'End', 'GeneSymbol', 'Type', 'Strand']).mean(), 2)
                Intersect = Intersect.fillna('NaN')
                Data_list.append(Intersect)

        if __name__ == '__main__':
            num_threads = 30
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
                executor.map(AllocateChr, Chromosome)

        Data = pd.concat(Data_list, axis = 0)
        Data = Data.sort_values(by=['Chromosome', 'Start','End'])
        Data = Data.reset_index()
        Data.to_csv(f'/labmed/06.AML/Result/04.Normal/231013.Methyl.{Prefix}.Personal.txt', sep='\t', index=False)

Calculate()

Annotate = pd.read_csv(f'/labmed/06.AML/Result/04.Normal/231013.Methyl.NCBI.RefSeq.Selected.hg19.Total.Personal.txt', sep='\t', header='infer')
Gene = Annotate.iloc[:, 0:6]

CR = Annotate.iloc[:, 6:18]
CR = round(CR.mean(axis=1), 2)
CR = CR.fillna('NaN')
CR = CR.replace('NaN', np.nan)

NR = Annotate.iloc[:, 18:30]
NR = round(NR.mean(axis=1), 2)
NR = NR.fillna('NaN')
NR = NR.replace('NaN', np.nan)

Normal = Annotate.iloc[:, 30:47]
Normal = round(Normal.mean(axis=1), 2)
Normal = Normal.fillna('NaN')
Normal = Normal.replace('NaN', np.nan)

CR_delta_NR = CR - NR
NR_delta_CR = NR - CR
CR_delta_Normal = CR - Normal
NR_delta_Normal = NR - Normal

result = pd.concat([Gene, CR, NR, Normal, CR_delta_NR, NR_delta_CR, CR_delta_Normal, NR_delta_Normal], axis=1)
result.columns = ['Chromosome', 'Start', 'End', 'GeneSymbol', 'Type', 'Strand', 'CR', 'NR', 'Normal', 'CR-NR', 'NR-CR', 'CR-Normal' ,'NR-Normal']

with pd.ExcelWriter('/labmed/06.AML/Result/04.Normal/231013.Methyl.Delta.xlsx') as writer:
    Data1 = result[result['CR-NR'] >= 10]
    Data1 = Data1.fillna('NaN')
    Data1.to_excel(writer, index=False, sheet_name='CR - NR')

    Data4 = result[result['NR-CR'] >= 10]
    Data4 = Data4.fillna('NaN')
    Data4.to_excel(writer, index=False, sheet_name='NR - CR')

    Data2 = result[result['CR-Normal'] >= 10]
    Data2 = Data2.fillna('NaN')
    Data2.to_excel(writer, index=False, sheet_name='CR - Normal')

    Data3 = result[result['NR-Normal'] >= 10]
    Data3 = Data3.fillna('NaN')
    Data3.to_excel(writer, index=False, sheet_name='NR - Normal')