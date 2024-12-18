#!/usr/bin/python3

import argparse
import sys
import pandas as pd
#------------------------------------------------------------------------------------------#
parser = argparse.ArgumentParser(description='Code Usage')
parser.add_argument('1', metavar='<bed>', help='Select bed file not include promoter')
args=parser.parse_args()
#------------------------------------------------------------------------------------------#
bed = pd.read_csv(sys.argv[1],
                  sep='\t',
                  header=None)

bed.loc[bed.iloc[:, 4] == '+', 1] -= 2000
bed.loc[bed.iloc[:, 4] == '-', 2] += 2000
#------------------------------------------------------------------------------------------#
BED = []
Chromosome = ['chr' + str(num) for num in range(1, 23)] + ['chrX', 'chrY']

def Intergenic(chromosome):
    Positive = bed[(bed.iloc[:, 0] == chromosome) & (bed.iloc[:, 4] == '+')]

    Start = Positive.iloc[:,2] + 1
    Start = Start.to_list()
    Start.pop(-1)

    End = Positive.iloc[:,1] - 1
    End = End.to_list()
    End.pop(0)

    Gene = ['Intergenic_' + str(Positive.iloc[i,3]) + '_' + str(Positive.iloc[i+1,3]) for i in range(Positive.shape[0]-1)]

    Positive = pd.DataFrame({'Chromosome' : chromosome,
                             'Start' : Start,
                             'End' : End,
                             'Gene' : 'NA',
                             'Region' : Gene,
                             'Strand' : '+'})
    BED.append(Positive)
    #------------------------------------------------------------------------------------------#
    Negative = bed[(bed.iloc[:, 0] == chromosome) & (bed.iloc[:, 4] == '-')]

    Start = Negative.iloc[:,2] + 1
    Start = Start.to_list()
    Start.pop(-1)

    End = Negative.iloc[:,1] - 1
    End = End.to_list()
    End.pop(0)

    Gene = ['Intergenic_' + str(Negative.iloc[i,3]) + '_' + str(Negative.iloc[i+1,3]) for i in range(Negative.shape[0]-1)]

    Negative = pd.DataFrame({'Chromosome' : chromosome,
                             'Start' : Start,
                             'End' : End,
                             'Gene' : 'NA',
                             'Region' : Gene,
                             'Strand' : '-'})
    BED.append(Negative)

list(map(Intergenic, Chromosome))
#------------------------------------------------------------------------------------------#
Total_Intergenic_bed = pd.concat(BED)
Total_Intergenic_bed = Total_Intergenic_bed.sort_values(['Chromosome', 'Start', 'End'])
Total_Intergenic_bed.to_csv('/media/src/hg19/01.Methylation/00.Bed/NCBI.RefSeq.Selected.Intergenic.bed',
                            sep='\t',
                            index=False,
                            header=None)
#------------------------------------------------------------------------------------------#