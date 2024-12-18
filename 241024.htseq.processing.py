import sys
import pandas as pd
#--------------------------------------------------------------------------#
Files = sys.argv[1:]

for order, cnt in enumerate(Files):
    if order == 0:
        Sample_name = cnt.split('_')[0]
        Data_first = pd.read_csv(cnt, sep='\t', header=None, names=['ID', Sample_name])
        Data_first = Data_first[Data_first['ID'].str.startswith('E')]
    else:
        Sample_name = cnt.split('_')[0]
        Data_rest = pd.read_csv(cnt, sep='\t', header=None, names=['ID', Sample_name])
        Data_rest = Data_rest[Data_rest['ID'].str.startswith('E')]
        Data_first = pd.merge(Data_first, Data_rest, on='ID')

GENE = pd.read_csv('/labmed/01.ALL/02.RNA/geneInfo.tab', sep='\t', header=None)
DICT = dict(zip(GENE[0], GENE[1]))

Data_first.insert(1, 'GeneSymbol', Data_first['ID'].map(DICT).fillna('Unknown'))
Data_first.to_csv('Varaser.readcnt.tsv', sep='\t', header='infer', index=False)