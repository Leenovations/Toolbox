import glob
import pandas as pd
#--------------------------------------------------------#

TSV = glob.glob('/labmed/01.AML/03.Common/00.GeneSet/*tsv')
TSV.sort()

for tsv in TSV:
    pathway = tsv.split('/')[-1]
    pathway = pathway.split('.')[0]
    Data = pd.read_csv(tsv,
                       sep='\t')
    Gene_list = Data.iloc[16,1].split(',')

    Gene_dataframe = pd.DataFrame({'Gene' : Gene_list})
    Gene_dataframe.to_csv(f"/labmed/01.AML/03.Common/00.GeneSet/{pathway}.Gene.List.txt",
                          sep='\t',
                          index=False)
    