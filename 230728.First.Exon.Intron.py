#!/usr/bin/python3

import pandas as pd
import multiprocessing
from multiprocessing import Pool
import time
from datetime import datetime
from natsort import natsorted
import os
import numpy as np
import pyranges as pr
#---------------------------------------------------------------------------------------------------#
now = datetime.now()
Start = time.time()
Date = now.strftime("%y%m%d")
#---------------------------------------------------------------------------------------------------#
Bed = pd.read_csv('/labmed/00.Code/00.Methylation/09.Ref/230720.Exon.Intron.table.comp.bed', sep='\t',
                  names=['Chromosome','Start','End','GeneSymbol','Region','Strand'])

Gene = list(set(Bed['GeneSymbol']))

def First_Exon(Gene_list):
    Gene_df = Bed[Bed['GeneSymbol'] == Gene_list]

    if Gene_df.iloc[0, 5] == '+':
        Gene_df = Gene_df.iloc[0:1]
        return Gene_df
    
    else:
        Index = Gene_df.shape[0] - 1
        Gene_df = Gene_df.iloc[Index:]
        return Gene_df

def First_Intron(Gene_list):
    Gene_df = Bed[Bed['GeneSymbol'] == Gene_list]

    if Gene_df.iloc[0, 5] == '+':
        Gene_df = Gene_df.iloc[1:2]
        return Gene_df
    
    else:
        Index = Gene_df.shape[0] - 1
        Gene_df = Gene_df.iloc[Index-1:Index]
        return Gene_df

def process_gene(gene_list, num_workers):
    with multiprocessing.Pool(processes=num_workers) as pool:
        gene_bed_list = pool.map(First_Exon, gene_list)
    return gene_bed_list

if __name__ == "__main__":
    num_workers = 30
    gene_bed_list = process_gene(Gene, num_workers)

    Exon_df = pd.concat(gene_bed_list, ignore_index=True)
    Exon_df.to_csv(f'/labmed/00.Code/00.Methylation/01.Output_table/{Date}.First.Exon.Unsorted.txt', sep='\t', index=False)
    Exon_df = Exon_df.iloc[natsorted(Exon_df.index, key=lambda x: (
    Exon_df.loc[x, 'Chromosome'],
    Exon_df.loc[x, 'Start'],
    Exon_df.loc[x, 'End']))]
    Exon_df.to_csv(f'/labmed/00.Code/00.Methylation/01.Output_table/{Date}.First.Exon.Sorted.txt', sep='\t', index=False)

def process_gene(gene_list, num_workers):
    with multiprocessing.Pool(processes=num_workers) as pool:
        gene_bed_list = pool.map(First_Intron, gene_list)
    return gene_bed_list

if __name__ == "__main__":
    num_workers = 30
    gene_bed_list = process_gene(Gene, num_workers)

    Intron_df = pd.concat(gene_bed_list, ignore_index=True)
    Intron_df.to_csv(f'/labmed/00.Code/00.Methylation/01.Output_table/{Date}.First.Intron.Unsorted.txt', sep='\t', index=False)
    Intron_df = Intron_df.iloc[natsorted(Intron_df.index, key=lambda x: (
    Intron_df.loc[x, 'Chromosome'],
    Intron_df.loc[x, 'Start'],
    Intron_df.loc[x, 'End']))]
    Intron_df.to_csv(f'/labmed/00.Code/00.Methylation/01.Output_table/{Date}.First.Intron.Sorted.txt', sep='\t', index=False)
#--------------------------------------------------------------------------------# Call CpG merged file
def CpG(txt, chunksize):
	CpG = pd.read_csv(txt, sep='\t', header=0, chunksize=chunksize, dtype={'Chromosome' : 'object'})
	dfs = []

	for chunk in CpG:
		dfs.append(chunk)

	df = pd.concat(dfs)
	return df

CR = CpG('/labmed/00.Code/00.Methylation/01.Output_table/230728.CpG.Merged.CR.txt', 5000000)
NR = CpG('/labmed/00.Code/00.Methylation/01.Output_table/230728.CpG.Merged.NR.txt', 5000000)
Normal = CpG('/labmed/00.Code/00.Methylation/01.Output_table/230721.CpG.Merged.Normal.txt', 50000000)
Col_Norm = list(Normal.columns[3:])
Normal[Col_Norm] = round(Normal[Col_Norm] * 100, 2)
#----------------------------------------------------------------------------------# Divide Small bin
def Ref(file_name:str):
    return pd.read_csv(f'/labmed/00.Code/00.Methylation/01.Output_table/{file_name}', sep='\t')

Reference = Ref('230728.First.Intron.Sorted.txt')
First_Gene = list(Reference['GeneSymbol'])

def GenePerBed(Gene):
    global Reference
    Gene_df = Reference[Reference['GeneSymbol'] == Gene]
    Bin = 5

    if Gene_df.iloc[0,5] == '+':
        Chromosome = Gene_df.iloc[0,0]
        Start = Gene_df.iloc[0,1]
        End = Gene_df.iloc[0,2]
        if End - Start != 0:
            # bins = np.arange(Start, End + 1, (End - Start) / Bin, dtype=int)
            # Start = bins[:-1]
            # End = bins[1:] - 1
            intervals = np.linspace(Start, End, Bin + 1, dtype=int)
            Start = intervals[:-1]
            End = intervals[1:]
            End[-1] = Gene_df.iloc[0,2]
            Order = list(range(0, Bin))
            Gene_Bed = pd.DataFrame({'Order' : Order, 'Chromosome' : Chromosome, 'Start': Start, 'End': End, 'GeneSymbol' : Gene})
            return Gene_Bed
    
    else:
        Chromosome = Gene_df.iloc[0,0]
        Start = Gene_df.iloc[0,1]
        End = Gene_df.iloc[0,2]
        if End - Start != 0:
            # bins = np.arange(Start, End + 1, (End - Start) / Bin, dtype=int)
            # Start = bins[:-1]
            # End = bins[1:] - 1
            intervals = np.linspace(Start, End, Bin + 1, dtype=int)
            Start = intervals[:-1]
            End = intervals[1:]
            End[-1] = Gene_df.iloc[0,2]
            
            Order = list(range(Bin-1, -1, -1))
            Gene_Bed = pd.DataFrame({'Order' : Order, 'Chromosome' : Chromosome, 'Start': Start, 'End': End, 'GeneSymbol' : Gene})
            return Gene_Bed


def process_gene(gene_list, num_workers):
    with multiprocessing.Pool(processes=num_workers) as pool:
        gene_bed_list = pool.map(GenePerBed, gene_list)
    return gene_bed_list

if __name__ == "__main__":
    num_workers = 20
    Gene_df = process_gene(First_Gene, num_workers)

Results = pd.concat(Gene_df, ignore_index=True)
Results = Results.iloc[:,[0,1,2,3]]
Results.to_csv('/labmed/00.Code/00.Methylation/01.Output_table/Table.test.txt', sep='\t', index=False)

def Cal(ref, cpg, region:str, group:str):
    Ref_bed = pr.PyRanges(ref)
    CpG_data = pr.PyRanges(cpg)
    Overlap = Ref_bed.join(CpG_data).df
    Overlap = Overlap.drop(['Chromosome', 'Start', 'End', 'Start_b', 'End_b'], axis=1)
    Data = round(Overlap.groupby('Order').mean(), 2)
    Data = Data.reset_index(drop=False, inplace=False)
    Data = Data.iloc[:,1:].mean(axis=1)
    Data = pd.DataFrame(Data)
    Data.columns=['Meth']
    Data['Meth'] = round(Data['Meth'], 2)
    Data['Order'] = list(range(0, Data.shape[0]))
    Data['Group'] = group
    Data.to_csv(f'/labmed/00.Code/00.Methylation/01.Output_table/{Date}.First.{region}.{group}.Methylation.txt', sep='\t', index=False)
    return Data

A = Cal(Results, CR, 'Intron', 'CR')
B = Cal(Results, NR, 'Intron', 'NR')
C = Cal(Results, Normal, 'Intron', 'Normal')

D = pd.concat([A, B, C])
D.to_csv(f'/labmed/00.Code/00.Methylation/01.Output_table/{Date}.First.Intron.Total.Methylation.txt', sep='\t', index=False)