#!/usr/bin/python3

import pandas as pd
import sys
import numpy as np

File = sys.argv[1]

Data = pd.read_csv(File, sep='\t', header = None)
print(Data)

Columns = sys.argv[2:]
Columns = list(map(int, Columns))
Columns = np.array(Columns)
Columns = Columns - 1
Columns = Columns.tolist()

Data = Data.drop(columns=Columns)
Data.to_csv(File, sep='\t', index=False, header=None)