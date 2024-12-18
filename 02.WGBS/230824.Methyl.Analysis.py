#!/usr/bin/python3

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
#-------------------------------------------------------------------------#
now = datetime.now()
Start = time.time()
Date = now.strftime("%y%m%d")
#-------------------------------------------------------------------------#
directories = ['Result/', 'Result/00.Tables/', 'Result/01.Plots/', 'Result/02.Bed/']

for directory in directories:
    if not os.path.isdir(directory):
        os.makedirs(directory)
#-------------------------------------------------------------------------#
Coverage_files = glob.glob('CpG/*cov')
Coverage_files.sort()

Coverage_list = []

def Check_Coverage(cov_file):
    Prefix = cov_file.split('/')[-1]
    Prefix = Prefix.split('.deduplicated.bismark.cov')[0]
    Coverage_file = pd.read_csv(cov_file, sep='\t', header=None)
    Coverage = Coverage_file.iloc[:, 4] + Coverage_file.iloc[:, 5]
    Mean_Coverage = round(np.mean(Coverage), 3)
    Median_Coverage = np.median(Coverage)
    Max_Coverage = max(Coverage)
    Min_Coverage = min(Coverage)

    Coverage_list.append(pd.DataFrame({'Sample' : [Prefix],
            'Mean Covarage' : [Mean_Coverage],
            'Median Coverage' : [Median_Coverage],
            'Max Coverage' : [Max_Coverage],
            'Min Coverage' : [Min_Coverage]}))
#-------------------------------------------------------------------------#
def Methylkit():
    command = f'Rscript /labmed/00.Code/03.WGBS/230808.Methylkit.R {sys.argv[5]} {sys.argv[1]} {sys.argv[2]}'
    os.system(command)
#-------------------------------------------------------------------------#
def Merge_CpG():
    bed_files = glob.glob(f"CpG/*.cov")
    bed_files.sort()

    Overlaps = [pd.read_csv(file, 
                         sep='\t', 
                         names=['Chromosome', 'Start', 'End', file.split('/')[-1].replace('.deduplicated.bismark.cov', '.per'), file.split('/')[-1].replace('.deduplicated.bismark.cov', '.meth') ,file.split('/')[-1].replace('.deduplicated.bismark.cov', '.unmeth')],
                         dtype={'Chromosome' : 'object'}, 
                         usecols=[0,1,2,3,4,5], 
                         index_col=False) for file in bed_files]

    filtered_overlaps = [overlap[(overlap.iloc[:,4] + overlap.iloc[:,5]) >= 5] for overlap in Overlaps]
    filtered_overlaps = [overlap.drop(overlap.columns[[4, 5]], axis=1) for overlap in filtered_overlaps]
    Overlaps_common = reduce(lambda left, right: pd.merge(left, right, on=['Chromosome', 'Start', 'End'], how='outer'), filtered_overlaps)
    Overlaps_common = Overlaps_common.fillna('NaN')
    Overlaps_common.to_csv(f'Result/00.Tables/CpG.Merged.txt', sep='\t', index=False)
#-------------------------------------------------------------------------#
def Calculate():
    Chromosome = ['chr' + str(number) for number in range(1,23)] + ['chrX', 'chrY']

    Bed_list = ['/media/src/hg19/01.Methylation/00.Bed/CGI.bed',
                '/media/src/hg19/01.Methylation/00.Bed/1MB.bed',
                '/media/src/hg19/01.Methylation/00.Bed/Inhancer.bed',
                '/media/src/hg19/01.Methylation/00.Bed/Promoter.bed',
                '/media/src/hg19/01.Methylation/00.Bed/LAD.bed',
                'Result/02.Bed/DMR.bed',
                '/media/src/hg19/01.Methylation/00.Bed/2kb.bed']

    Merged_CpG = pd.read_csv(f'Result/00.Tables/CpG.Merged.txt', sep='\t', header='infer')

    for bed in Bed_list:
        Prefix = bed.split('/')[-1]
        Prefix = Prefix.split('.bed')[0]
        Data_list = []
        bed = pd.read_csv(bed, sep='\t', header=None)

        def AllocateChr(chromosome): 
            if chromosome in list(Merged_CpG['Chromosome'].drop_duplicates()) and chromosome in list(bed[0].drop_duplicates()):
                MergeSubset = Merged_CpG[Merged_CpG.iloc[:, 0] == chromosome]
                Subset = bed[bed.iloc[:, 0] == chromosome]
                Subset.columns = ['Chromosome','Start','End']
                pySubset = pr.PyRanges(Subset)
                pyMerged = pr.PyRanges(MergeSubset)

                Intersect = pySubset.join(pyMerged).df
                Intersect = Intersect.drop(['Start_b', 'End_b'], axis=1)
                Intersect = Intersect.astype({'Chromosome': 'str', 'Start' : 'int', 'End' : 'int'}) 	
                Intersect = round(Intersect.groupby(['Chromosome', 'Start', 'End']).mean(), 3)
                Intersect = Intersect.fillna('NaN')
                Data_list.append(Intersect)

        if __name__ == '__main__':
            num_threads = int(sys.argv[5])
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
                executor.map(AllocateChr, Chromosome)

        Data = pd.concat(Data_list, axis = 0)
        Data = Data.sort_values(by=['Chromosome', 'Start','End'])
        Data = Data.reset_index()
        Data.to_csv(f'Result/00.Tables/Methyl.{Prefix}.Personal.txt', sep='\t', index=False)
#-------------------------------------------------------------------------#
def Densityplot():
    Data = pd.read_csv('Result/00.Tables/Methyl.2kb.Personal.txt', sep='\t', header='infer')

    Group1 = round(Data.iloc[:,3:int(sys.argv[1])].mean(axis=1), 2)
    Group2 = round(Data.iloc[:,int(sys.argv[1]):].mean(axis=1), 2)
    Group = pd.concat([Group1, Group2], axis=1)
    Group.columns = [str(sys.argv[3]), str(sys.argv[4])]
    Total = pd.concat([Data.iloc[:,0:3], Group], axis=1)
    Total = Total.fillna('NaN')
    Total.to_csv(f'Result/00.Tables/Methyl.2kb.Group.txt', sep='\t', index=False)
#------------------------------------------------------------------------#
def Density():
    command = f'Rscript /labmed/00.Code/03.WGBS/Methyl.Density.Plot.R {sys.argv[3]} {sys.argv[4]}'
    os.system(command)
#------------------------------------------------------------------------#
def PCA():
    command = f'Rscript /labmed/00.Code/03.WGBS/PCA.R {sys.argv[3]} {sys.argv[4]} {int(sys.argv[1])} {int(sys.argv[2])}'
    os.system(command)
#------------------------------------------------------------------------#
def Heatmap():
    command = f'Rscript /labmed/00.Code/03.WGBS/Methyl.Heatmap.R {sys.argv[3]} {sys.argv[4]} {int(sys.argv[1])} {int(sys.argv[2])}'
    os.system(command)
#------------------------------------------------------------------------#
def Boxplot():
    Bed_list = ['Result/00.Tables/Methyl.1MB.Personal.txt',
                'Result/00.Tables/Methyl.CGI.Personal.txt',
                'Result/00.Tables/Methyl.DMR.Personal.txt',
                'Result/00.Tables/Methyl.Inhancer.Personal.txt',
                'Result/00.Tables/Methyl.LAD.Personal.txt',
                'Result/00.Tables/Methyl.Promoter.Personal.txt']
    Box_list = []

    def Processing(cal_file):
        Type = cal_file.split('/')[-1]
        Type = Type.split('.')[2]
        Data = pd.read_csv(cal_file, sep='\t', header='infer')
        Data = Data.iloc[:, 3:]
        Data = Data.mean(axis=0)

        Data = Data.reset_index()
        Data.columns = ['Sample', 'Meth']
        Data['Group'] = [f'{sys.argv[3]}'] * int(sys.argv[1]) + [f'{sys.argv[4]}'] * int(sys.argv[2])
        Data['Type'] = Type
        
        Data = pd.DataFrame(Data)
        Box_list.append(Data)

    list(map(Processing, Bed_list))

    Data = pd.concat(Box_list, axis = 0)
    Data.to_csv('Result/00.Tables/Multiple_Boxplot.txt', sep='\t', index=False, header=True)
    with pd.ExcelWriter('Result/00.Tables/Analysis.Table.xlsx', engine="openpyxl", mode='a') as writer: 
        Data.to_excel(writer, sheet_name='Mean Methylation', header=True, index=False)
#------------------------------------------------------------------------#
def MultiBoxplot():
    command = f'Rscript /labmed/00.Code/03.WGBS/Multiple.Boxplot.R'
    os.system(command)
#------------------------------------------------------------------------#
def HOMMER():
    command = f'findMotifsGenome.pl Result/02.Bed/Hyper.DMR.bed hg19 Result/03.HOMER/00.Hyper'
    os.system(command)

    command = f'findMotifsGenome.pl Result/02.Bed/Hypo.DMR.bed hg19 Result/03.HOMER/01.Hypo'
    os.system(command)
#------------------------------------------------------------------------#
def GeneLintPlot():
    pass
#------------------------------------------------------------------------#
HGMD = pd.read_csv('/media/src/hg19/01.Methylation/00.Bed/NCBI.RefSeq.Selected.±.5kb.Gene.bed',
                sep='\t',
                names=['Chromosome', 'Start', 'End', 'GeneSymbol', 'Strand'])

DMR = pd.read_csv('/labmed/06.AML/Result/00.Tables/Methylkit.Annotation.txt',
                sep='\t',
                header='infer')

Hyper_Gene = DMR[DMR['DMR']=='hyper'].loc[:, 'annot.symbol']
Hyper_Gene = Hyper_Gene.dropna()
Hyper_Gene = set(Hyper_Gene)

Hypo_Gene = DMR[DMR['DMR']=='hypo'].loc[:, 'annot.symbol']
Hypo_Gene = Hypo_Gene.dropna()
Hypo_Gene = set(Hypo_Gene)

Gene_list = set(HGMD['GeneSymbol'])

DMR_Gene = list((Hyper_Gene | Hypo_Gene) & Gene_list)

Gene_df = []

if os.path.isdir('Result/02.Bed/00.Geneplot'):
    pass
else:
    command = 'mkdir Result/02.Bed/00.Geneplot'
    os.system(command)

def GenePerBed(Gene):
    Ref = HGMD.copy() 
    Ref = Ref[Ref['GeneSymbol'] == Gene]

    Chromosome = Ref.iloc[0,0]
    Start = Ref.iloc[0,1]
    End = Ref.iloc[0,2]
    Bin = 100
    bins = np.arange(Start, End + 1, (End - Start) / Bin, dtype=int)
    Start = bins[:-1]
    End = bins[1:] - 1
    End[-1] = Ref.iloc[0,2]
    Gene_Bed = pd.DataFrame({'Chromosome' : Chromosome, 'Start': Start, 'End': End, 'GeneSymbol' : Gene})
    Gene_Bed.to_csv(f'Result/02.Bed/00.Geneplot/{Gene}.{str(Bin)}bin.bed',
                    sep='\t',
                    index=False)
    return Gene_Bed

def process_gene(gene_list, num_workers):
    with multiprocessing.Pool(processes=num_workers) as pool:
        gene_bed_list = pool.map(GenePerBed, gene_list)
    return gene_bed_list

if __name__ == "__main__":
    num_workers = 30
    Gene_df = process_gene(DMR_Gene, num_workers)
#------------------------------------------------------------------------#
if os.path.isdir('Result/00.Tables/00.GenePlot'):
    pass
else:
    command = 'mkdir Result/00.Tables/00.GenePlot'
    os.system(command)

Case = pd.read_csv(f'Result/00.Tables/CpG.Merged.txt', sep='\t', header='infer')
Case = pr.PyRanges(Case)

def Cal_Case(Df_list):
    GeneSymbol = list(Df_list['GeneSymbol'])[0]
    print(GeneSymbol)
    Df_list.drop('GeneSymbol', axis=1, inplace=True)
    Bed = pr.PyRanges(Df_list)
    global Case
    Overlap = Bed.join(Case).df
    if 'Start_b' in Overlap.columns:
        Overlap = Overlap.drop(['Start_b', 'End_b'], axis=1)
        Overlap = Overlap.astype({'Chromosome': 'str', 'Start' : 'int', 'End' : 'int'}) 	
        Data = round(Overlap.groupby(['Chromosome', 'Start', 'End']).mean(),2)
        Data['Meth_CR'] = round(Data.iloc[:,4:16].mean(axis=1), 2) #sys.argv
        Data['Meth_NR'] = round(Data.iloc[:,16:28].mean(axis=1), 2) #sys.argv
        Data = Data.reset_index()
        Data_CR = Data.iloc[:, [0, 1, 2, -2]].copy()
        Data_CR['Group'] = 'CR'
        Data_NR = Data.iloc[:, [0, 1, 2, -1]].copy()
        Data_NR['Group'] = 'NR'

        A = Data_CR.to_csv(f'Result/00.Tables/00.GenePlot/{GeneSymbol}.CR.avg.txt', sep='\t', index=False) #sys.argv
        B = Data_NR.to_csv(f'Result/00.Tables/00.GenePlot/{GeneSymbol}.NR.avg.txt', sep='\t', index=False) #sys.argv
        return A, B

def process_gene(gene_list, num_workers):
    with multiprocessing.Pool(processes=num_workers) as pool:
        gene_bed_list = pool.map(Cal_Case, gene_list)
    return gene_bed_list

if __name__ == "__main__":
    num_workers = 30
    process_gene(Gene_df, num_workers)
#------------------------------------------------------------------------#
#------------------------------------------------------------------------#
#------------------------------------------------------------------------#
if sys.argv[6] == 'All':
    Coverage_files = glob.glob('CpG/*cov')
    Coverage_files.sort()

    Coverage_list = []

    if __name__ == '__main__':
        num_threads = int(sys.argv[5])
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            executor.map(Check_Coverage, Coverage_files)
        
    Data = pd.concat(Coverage_list)
    Data.to_excel(f'Result/00.Tables/Analysis.Table.xlsx', sheet_name='Coverage', index=False)

    print('\n', "\033[91m Coverage Completed!!\033[0m", '\n')

    Methylkit()
    print('\n', "\033[91m Methylkit Completed!!\033[0m", '\n')

    Merge_CpG()
    print('\n', "\033[91m CpG Merge Completed!!\033[0m", '\n')
    Calculate()
    print('\n', "\033[91m CpG Calculation Completed!!\033[0m", '\n')
    Densityplot()
    print('\n', "\033[91m Making Density table Completed!!\033[0m", '\n')

    Density()
    print('\n', "\033[91m Drawing Density plot Completed!!\033[0m", '\n')
    PCA()
    print('\n', "\033[91m Drawing PCA plot Completed!!\033[0m", '\n')
    Heatmap()
    print('\n', "\033[91m Drawing Heatmap plot Completed!!\033[0m", '\n')

    Boxplot()
    print('\n', "\033[91m Making boxplot table Completed!!\033[0m", '\n')
    MultiBoxplot()
    print('\n', "\033[91m Drawing Multiple boxplot Completed!!\033[0m", '\n')

    HOMMER()
    print('\n', "\033[91m HOMMER Completed!!\033[0m", '\n')
    
elif sys.argv[6] == 'Coverage':
    Coverage_files = glob.glob('CpG/*cov')
    Coverage_files.sort()

    Coverage_list = []

    if __name__ == '__main__':
        num_threads = int(sys.argv[5])
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            executor.map(Check_Coverage, Coverage_files)
        
    Data = pd.concat(Coverage_list)
    Data.to_excel(f'Result/00.Tables/Analysis.Table.xlsx', sheet_name='Coverage', index=False)
    Data.to_excel(f'Result/00.Tables/Analysis.Table.xlsx', sheet_name='Coverage', index=False)

elif sys.argv[6] == 'DMR':
    Methylkit()
    print('\n', "\033[91m Methylkit Completed!!\033[0m", '\n')

elif sys.argv[6] == 'Caluculation':
    Merge_CpG()
    print('\n', "\033[91m CpG Merge Completed!!\033[0m", '\n')
    Calculate()
    print('\n', "\033[91m CpG Calculation Completed!!\033[0m", '\n')
    Densityplot()
    print('\n', "\033[91m Making Density table Completed!!\033[0m", '\n')
    Boxplot()
    print('\n', "\033[91m Making boxplot table Completed!!\033[0m", '\n')

elif sys.argv[6] == 'HOMER':
    HOMMER()
    print('\n', "\033[91m HOMMER Completed!!\033[0m", '\n')

elif sys.argv[6] == 'Drawing':
    # Density()
    # print('\n', "\033[91m Drawing Density plot Completed!!\033[0m", '\n')
    # PCA()
    # print('\n', "\033[91m Drawing PCA plot Completed!!\033[0m", '\n')
    # Heatmap()
    # print('\n', "\033[91m Drawing Heatmap plot Completed!!\033[0m", '\n')
    # MultiBoxplot()
    # print('\n', "\033[91m Drawing Multiple boxplot Completed!!\033[0m", '\n')
    GeneLintPlot()
#------------------------------------------------------------------------#
End = time.time()
Execution = round(float(End - Start) / 60, 2)
print(f'Run Time : {Execution}min')