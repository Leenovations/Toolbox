#!/home/lab/anaconda3/envs/NGS/bin/python3

import pandas as pd
import numpy as np
import pyranges as pr
#-------------------------------------------------------------------------------------#
Header = pd.read_csv('/labmed/01.AML/01.WGBS/00.Header/Header.txt',
                     sep='\t',
                     header='infer')
Header_WGBS = Header['WGBS']
Header_WGBS = Header_WGBS.dropna()
Header_WGBS = Header_WGBS.to_list()
#-------------------------------------------------------------------------------------#
def Cal(bed, prefix, *colnames):
    columnnames = list(colnames)

    Bed = pd.read_csv(bed,
                    sep='\t',
                    names=columnnames)
    pyBed = pr.PyRanges(Bed)
    #-------------------------------------------------------------------------------------#
    Data = pd.read_csv('/labmed/01.AML/01.WGBS/240119.AML.150bp.Methyl.txt',
                    sep='\t',
                    low_memory=False)
    Data.columns = ['Chromosome', 'Start', 'End', 'Strand'] + Header_WGBS

    pyData = pr.PyRanges(Data)

    Intersect = pyBed.join(pyData).df
    Intersect = Intersect.drop(['Start_b', 'End_b'], axis=1)
    Intersect = Intersect.astype({'Chromosome': 'str', 'Start' : 'int', 'End' : 'int', 'Strand' : 'str'})
    Intersect = Intersect.groupby(['Chromosome', 'Start', 'End', 'Strand'], as_index=False).mean().round(2)
    Intersect = Intersect.fillna('NaN')

    Intersect.to_csv(f'/labmed/01.AML/01.WGBS/240205.AML.150bp.{prefix}.Methyl.txt',
                    sep='\t',
                    index=False)

    Intersect_mean = Intersect.mean()
    Intersect_mean.to_csv(f'/labmed/01.AML/01.WGBS/240205.AML.150bp.{prefix}.Mean.Methyl.txt',
                        sep='\t',
                        header='infer',
                        index=False)
    #-------------------------------------------------------------------------------------#
Cal('/media/src/hg19/01.Methylation/00.Bed/1000000bp.bed', '1MB', 'Chromosome', 'Start', 'End')