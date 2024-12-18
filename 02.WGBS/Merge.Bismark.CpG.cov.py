#!/usr/bin/python3

import pandas as pd
import pyranges as pr

from collections import ChainMap

CR_names = ['CR_' + str(num) + '.cov' for num in range(1, 13)]
NR_names = ['NR_' + str(num) + '.cov' for num in range(1, 13)]

Cov_files =  CR_names + NR_names

Merged = pd.read_csv(Cov_files[0], sep='\t', header=None)

for cov in Cov_files[1:]:
    cov = pd.read_csv(cov, sep='\t', header=None)
    Merged = pd.merge(Merged, cov, how='outer', on=[0,1,2], sort=True)

Merged = Merged.fillna('NaN')
Merged.to_csv('AML.Merged.cov', header=None, sep='\t', index=False)
