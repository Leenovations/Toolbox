import os
import gzip
import glob
import pandas as pd
#----------------------------------------------------------------------------------#
Data = sorted(glob.glob('/media/src/hg19/08.bed/*HMM.tsv'))
#----------------------------------------------------------------------------------#
for hmm in Data:
    prefix = hmm.split('/')[-1]
    prefix = prefix.split('HMM.tsv')[0]
    #----------------------------------------------------------------------------------#    
    Data = pd.read_csv(hmm,
                       sep='\t',
                       header='infer')
    Data['name'] = Data['name'].apply(lambda x: '_'.join(x.split('_', )[1:]))
    Data.columns = ['Chromosome', 'Start', 'End', 'Region']
    Data = Data.sort_values(by=['Chromosome', 'Start', 'End'])
    Data.to_csv(f'/media/src/hg19/08.bed/chromHMM.{prefix}.tsv',
                sep='\t',
                header='infer',
                index=False)