#!/home/lab/anaconda3/envs/NGS/bin/python3

import argparse
import pandas as pd
import numpy as np
#----------------------------------------------------------------------------------------#
Sample = ['CR_AYB',
            'CR_HJJ',
            'CR_JJB',
            'CR_JTN',
            'CR_KDS',
            'CR_KYK',
            'CR_LJP',
            'CR_LKB',
            'CR_LKH',
            'CR_NKYY',
            'CR_SYK',
            'CR_YSJ',
            'NR_HSW',
            'NR_JMJ',
            'NR_JWS',
            'NR_KKY',
            'NR_KWH',
            'NR_KYS',
            'NR_LHB',
            'NR_LMS',
            'NR_PHS',
            'NR_PMK',
            'NR_SWSJ',
            'NR_YDM']
#----------------------------------------------------------------------------------------#
SAMPLE = ['Chromosome', 'Start', 'End', 'Strand']
for samp in Sample:
    SAMPLE.append(samp + '_Cov')
    SAMPLE.append(samp + '_Cs')
    SAMPLE.append(samp + '_Ts')
#----------------------------------------------------------------------------------------#
Data = pd.read_csv('/media/node01-HDD01/00.AML/01.Results/240119.AML.150bp.txt',
                   sep='\t',
                   header=None,
                   names=SAMPLE)
#----------------------------------------------------------------------------------------#
df_filtered = Data.drop(columns=[col for col in Data.columns if '_Ts' in col])
#----------------------------------------------------------------------------------------#
DATA = pd.DataFrame()
for i in range(4, len(df_filtered.columns), 2):
    DATA[df_filtered.columns[i].replace('_Cov', '')] = round(df_filtered.iloc[:, i+1] / df_filtered.iloc[:, i] * 100, 2)
#----------------------------------------------------------------------------------------#
Merged = pd.concat([Data.iloc[:,0:4], DATA], axis=1)
Merged.to_csv('/media/node01-HDD01/00.AML/01.Results/240119.AML.150bp.test.Methyl.txt',
              sep='\t',
              header='infer',
              index=False)
#----------------------------------------------------------------------------------------#
CR = round(Merged.iloc[:, 4:16].mean(axis=1), 2)
NR = round(Merged.iloc[:, 16:].mean(axis=1), 2)
Diff = round(CR - NR, 2)
Mean = pd.concat([Data.iloc[:,0:4], CR, NR, Diff], axis=1)
Mean.columns = ['Chromosome', 'Start', 'End', 'Strand', 'CR', 'NR', 'CR-NR']
Mean.to_csv('/media/node01-HDD01/00.AML/01.Results/240119.AML.150bp.Mean.Diff.Methyl.txt',
              sep='\t',
              header='infer',
              index=False)
#----------------------------------------------------------------------------------------#
CR = round(Merged.iloc[:, 4:16].mean(axis=1), 2)
NR = round(Merged.iloc[:, 16:].mean(axis=1), 2)
Diff = round(CR - NR, 2)
Diff = pd.concat([Data.iloc[:,0:4], Diff], axis=1)
Diff.columns = ['Chromosome', 'Start', 'End', 'Strand', 'CR-NR']
Diff.to_csv('/media/node01-HDD01/00.AML/01.Results/240119.AML.150bp.Diff.Methyl.txt',
              sep='\t',
              header='infer',
              index=False)
#----------------------------------------------------------------------------------------#