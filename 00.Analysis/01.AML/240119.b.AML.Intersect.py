#!/home/lab/anaconda3/envs/NGS/bin/python3

import pandas as pd
import numpy as np
import pyranges as pr
#----------------------------------------------------------------------------------------#
# Genelist = ['TAL1', 'BCL11A', 'GATA1', 'GATA2', 'NFE2']
Genelist = ['TLR1', 'TLR2', 'TLR3', 'TLR4', 'TLR5', 'TLR6', 'TLR7', 'TLR8', 'CD8A', 'CD8B', 'CTLA4']
for gene in Genelist:
    Bed = pd.read_csv('/media/src/hg19/01.Methylation/00.Bed/NCBI.RefSeq.Selected.±.5kb.Gene.bed',
                    sep='\t',
                    names=['Chromosome', 'Start', 'End', 'Gene', 'Strand'])
    Bed = Bed.drop(['Strand'], axis=1)
    Bed = Bed[Bed['Gene'] == gene]
    pyBed = pr.PyRanges(Bed)
    #-------------------------------------------------------------------------------------#
    Data = pd.read_csv('/media/node01-HDD01/00.AML/01.Results/240119.AML.150bp.Mean.Diff.Methyl.txt',
                    sep='\t',
                    header='infer')

    pyData = pr.PyRanges(Data)

    Intersect = pyData.join(pyBed).df
    Intersect = Intersect.drop(['Start_b', 'End_b'], axis=1)

    Intersect.to_csv(f'/media/node01-HDD01/00.AML/01.Results/240119.AML.150bp.{gene}.Methyl.txt',
                    sep='\t',
                    index=False)
    #-------------------------------------------------------------------------------------#