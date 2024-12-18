#!/usr/bin/python3

import os
import glob
import pandas as pd
import argparse
import sys
import concurrent.futures
import pyranges as pr
#-------------------------------------------------------------------------------------#
parser = argparse.ArgumentParser(description="Code Usage")
parser.add_argument('1', metavar='<bed>', help='Select Bed file')
parser.add_argument('2', metavar='<Prefix>', help='Set prefix')
parser.add_argument('3', metavar='<Meth value>', help='Set Methylation Difference')
parser.add_argument('4', metavar='<Group>',nargs='+', help='Select bed file for position annotation ex) CR NR 12 12 ...')
args=parser.parse_args()
#-------------------------------------------------------------------------------------#
# if os.path.isdir('CpG/02.Intersect/'):
#     pass
# else:
#     command = 'mkdir CpG/02.Intersect/'
#     os.system(command)
# #-------------------------------------------------------------------------------------#
# File = glob.glob('CpG/01.Trim/*cov')
# File.sort()
# #-------------------------------------------------------------------------------------#
# Bed = sys.argv[1]
# Bed = pd.read_csv(Bed,
#                   sep='\t',
#                   names=['Chromosome', 'Start', 'End', 'Gene', 'Region', 'ID', 'Strand'])
# pyBed = pr.PyRanges(Bed)
# #-------------------------------------------------------------------------------------#
# def Meth(cov):
#     Name = cov.split('/')[-1]
#     Name = Name.replace('.trim.cov', '')
#     Data = pd.read_csv(cov,
#                        sep='\t',
#                        names = ['Chromosome', 'Start', 'End', f'{Name}'])
    
#     pyData = pr.PyRanges(Data)

#     Intersect = pyBed.join(pyData).df
#     Intersect = Intersect.drop(['Start_b', 'End_b'], axis=1)
#     Intersect = Intersect.astype({'Chromosome': 'str', 'Start' : 'int', 'End' : 'int', 'Gene' : 'str', 'Region' : 'str', 'ID' : 'str', 'Strand' : 'str', Data.columns[3] :'float'})
#     Intersect = round(Intersect.groupby(['Chromosome', 'Start', 'End', 'Gene', 'Region', 'ID', 'Strand']).mean(), 2)
#     Intersect = Intersect.reset_index()
#     Intersect['Strand'] = Intersect['Strand'].replace('nan', '*')

#     Intersect.to_csv(f'CpG/02.Intersect/{Data.columns[3]}.{sys.argv[2]}.cov',
#                      sep='\t',
#                      index=False)
# list(map(Meth, File))
# #-------------------------------------------------------------------------------------#
# if os.path.isdir('CpG/04.Merged'):
#     pass
# else:
#     os.makedirs('CpG/04.Merged', exist_ok=False)
# #-------------------------------------------------------------------------------------#
# Annotated = glob.glob('CpG/02.Intersect/*cov')
# Annotated.sort()
# #-------------------------------------------------------------------------------------#
# CommonColumns = []
# def ReadCovFile(cov):
#     Data = pd.read_csv(cov,
#                        sep='\t',
#                        header='infer')
#     CommonColumns.append(Data)
#     Data.fillna('NA', inplace=True)

# list(map(ReadCovFile, Annotated))
# #-------------------------------------------------------------------------------------#
# Common_Data = pd.concat(CommonColumns, axis=0)
# Common_Data = round(Common_Data.groupby(['Chromosome', 'Start', 'End', 'Gene', 'Region', 'ID', 'Strand']).mean(), 2)
# Common_Data.reset_index(inplace=True)
# Common_Data.fillna('NA', inplace=True)
# #-------------------------------------------------------------------------------------#
# Common_Data.to_csv(f'CpG/04.Merged/Total.cov',
#                     sep='\t',
#                     index=False)
#-------------------------------------------------------------------------------------#
Common_Data = pd.read_csv('CpG/04.Merged/Total.cov',
                          sep='\t',
                          header='infer')
Common_Data.insert(7, 'NA Count', Common_Data.iloc[:,7:].isna().sum(axis=1))
#-------------------------------------------------------------------------------------#
Common_Data_subset = Common_Data[Common_Data.iloc[:,7]==0].iloc[:,8:]
#-------------------------------------------------------------------------------------#
Group_info = sys.argv[4:]
Group_name = Group_info[0:int(len(Group_info)/2)]
Group_ID = Group_info[0:int(len(Group_info)/2)]
Group_number = Group_info[int(len(Group_info)/2):]

def MeanMethylation():
    Start = 0
    End = int(Group_number[0])
    global MEAN
    MEAN = []

    for id in range(len(Group_ID)):
        if id + 1 < len(Group_name):
            Group_ID[id] = round(Common_Data_subset.iloc[:, Start:End].mean(axis=1), 2)
            Start = End
            End = End + int(Group_number[id+1])
            MEAN.append(Group_ID[id])
        elif id + 1 >= len(Group_name):
            Group_ID[id] = round(Common_Data_subset.iloc[:, Start:End].mean(axis=1), 2)
            MEAN.append(Group_ID[id])

MeanMethylation()
#-------------------------------------------------------------------------------------#
excel_writer = pd.ExcelWriter(f'CpG/04.Merged/Annotation.Diff.{sys.argv[3]}.xlsx')
#-------------------------------------------------------------------------------------#
Total = pd.DataFrame(pd.concat(MEAN, axis=1))
Total.columns = Group_name
Total_info = pd.concat([Common_Data[Common_Data.iloc[:,7]==0].iloc[:,:8], Total], axis=1)
#-------------------------------------------------------------------------------------#
# Total_info.to_excel(excel_writer, sheet_name = 'Mean Annotation', index=False)
#-------------------------------------------------------------------------------------#
#CR - NR >= int(sys.argv[3]) -> CR Hypermethylation
Delta = Total_info[Total_info['CR'] - Total_info['NR'] >= int(sys.argv[3])]
Gene = Delta.iloc[:,3].dropna().unique().tolist()
Gene = pd.DataFrame(Gene, columns=['CR Hyper Gene'])
#-------------------------------------------------------------------------------------#
Delta.to_excel(excel_writer, sheet_name = 'CR Hypermethylation', index=False)
Gene.to_excel(excel_writer, sheet_name = 'CR Hypermethylation Gene', index=False)
#-------------------------------------------------------------------------------------#
#NR - CR >= int(sys.argv[3]) -> NR Hypermethylation
Delta = Total_info[Total_info['NR'] - Total_info['CR'] >= int(sys.argv[3])]
Gene = Delta.iloc[:,3].dropna().unique().tolist()
Gene = pd.DataFrame(Gene, columns=['NR Hyper Gene'])
#-------------------------------------------------------------------------------------#
Delta.to_excel(excel_writer, sheet_name = 'NR Hypermethylation', index=False)
Gene.to_excel(excel_writer, sheet_name = 'NR Hypermethylation Gene', index=False)
# #-------------------------------------------------------------------------------------#
# #CR & Normal - NR >= int(sys.argv[3])
# Delta = Total_info[(Total_info['CR'] - Total_info['NR'] >= int(sys.argv[3])) & (Total_info['Normal'] - Total_info['NR'] >= int(sys.argv[3]))]
# Gene = Delta.iloc[:,3].dropna().unique().tolist()
# Gene = pd.DataFrame(Gene, columns=['CR & Normal Hyper Gene'])
# #-------------------------------------------------------------------------------------#
# Delta.to_excel(excel_writer, sheet_name = 'CR & Normal Hyper.sim', index=False)
# Gene.to_excel(excel_writer, sheet_name = 'CR & Normal Hyper.sim Gene', index=False)
# #-------------------------------------------------------------------------------------#
#CR - NR >= int(sys.argv[3]) -> CR Hypomethylation
Delta = Total_info[Total_info['CR'] - Total_info['NR'] <= -int(sys.argv[3])]
Gene = Delta.iloc[:,3].dropna().unique().tolist()
Gene = pd.DataFrame(Gene, columns=['CR Hypo Gene'])
#-------------------------------------------------------------------------------------#
Delta.to_excel(excel_writer, sheet_name = 'CR Hypomethylation', index=False)
Gene.to_excel(excel_writer, sheet_name = 'CR Hypomethylation Gene', index=False)
#-------------------------------------------------------------------------------------#
#NR - CR >= int(sys.argv[3]) -> NR Hypomethylation
Delta = Total_info[Total_info['NR'] - Total_info['CR'] <= -int(sys.argv[3])]
Gene = Delta.iloc[:,3].dropna().unique().tolist()
Gene = pd.DataFrame(Gene, columns=['NR Hypo Gene'])
#-------------------------------------------------------------------------------------#
Delta.to_excel(excel_writer, sheet_name = 'NR Hypomethylation', index=False)
Gene.to_excel(excel_writer, sheet_name = 'NR Hypomethylation Gene', index=False)
# #-------------------------------------------------------------------------------------#
# #CR & Normal - NR >= int(sys.argv[3])
# Delta = Total_info[(Total_info['CR'] - Total_info['NR'] <= -int(sys.argv[3])) & (Total_info['Normal'] - Total_info['NR'] <= -int(sys.argv[3]))]
# Gene = Delta.iloc[:,3].dropna().unique().tolist()
# Gene = pd.DataFrame(Gene, columns=['CR & Normal Hypo Gene'])
# #-------------------------------------------------------------------------------------#
# Delta.to_excel(excel_writer, sheet_name = 'CR & Normal Hypo.sim', index=False)
# Gene.to_excel(excel_writer, sheet_name = 'CR & Normal Hypo.sim Gene', index=False)
# #-------------------------------------------------------------------------------------#
excel_writer.close()