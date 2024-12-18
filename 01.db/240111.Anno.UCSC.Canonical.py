#!/home/lab/anaconda3/envs/NGS/bin/python3

import pandas as pd
#------------------------------------------------#
Data = pd.read_csv('/media/src/hg19/06.Annotation/UCSC.knownCanonical.hg19.txt',
                   sep='\t',
                   header='infer')
#------------------------------------------------#
Data = Data.dropna()
#------------------------------------------------#
Data = Data.iloc[:,5:7]
#------------------------------------------------#
Data.columns = ['GeneSymbol', 'NM_number']
#------------------------------------------------#
Data.to_csv('/media/src/hg19/06.Annotation/UCSC.hg19.Canonical.NMnumber.txt',
            sep='\t',
            index=False,
            header='infer')
#------------------------------------------------#