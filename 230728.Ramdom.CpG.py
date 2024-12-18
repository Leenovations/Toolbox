#!/usr/bin/python3

import pandas as pd

# CpG = pd.read_csv('/labmed/00.Code/00.Methylation/01.Output_table/230721.CpG.Merged.Normal.txt', sep='\t')

# Random_CpG = CpG.sample(n=100000)

# Random_CpG.to_csv('/labmed/00.Code/00.Methylation/01.Output_table/230728.Random.Case.CpG.txt', index=False, sep='\t') 

# Normal = pd.read_csv('/labmed/00.Code/00.Methylation/01.Output_table/230721.CpG.Merged.bismark.txt', sep='\t')

# Random_Normal = CpG.sample(n=100000)

# Random_CpG.to_csv('/labmed/00.Code/00.Methylation/01.Output_table/230728.Random.Normal.CpG.txt', index=False, sep='\t') 

# CpG = pd.read_csv('/labmed/00.Code/00.Methylation/01.Output_table/230721.CpG.Merged.Normal.txt', sep='\t')

# Random_CpG = CpG.sample(n=100000)

# Random_CpG.to_csv('/labmed/00.Code/00.Methylation/01.Output_table/230728.Random.Case.CpG.txt', index=False, sep='\t') 

CpG = pd.read_csv('/labmed/00.Code/00.Methylation/01.Output_table/230721.CpG.Merged.bismark.txt', sep='\t')
CpG0 = CpG.iloc[:, 0:15]
CpG0.to_csv('/labmed/00.Code/00.Methylation/01.Output_table/230728.CpG.Merged.CR.txt', index=False, sep='\t') 

print(CpG0.shape[1])

CpG1 = CpG.iloc[:, 0:3]1
CpG2 = CpG.iloc[:, 15:

A = pd.concat([CpG1, CpG2], axis=1)
A.to_csv('/labmed/00.Code/00.Methylation/01.Output_table/230728.CpG.Merged.NR.txt', index=False, sep='\t') 
print(A.shape[1])