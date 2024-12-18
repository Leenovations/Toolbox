#!/usr/bin/python3

import pandas as pd
import os
import argparse
import sys

#----------------------------------------------------------------------------------------#
parser = argparse.ArgumentParser(description='Pipeline Usage')
parser.add_argument('1', metavar='<Input>', help='Input file')
parser.add_argument('2', metavar='<Output>', help='Output file')
args = parser.parse_args()
# ----------------------------------------------------------------------------------------#
Data = pd.read_csv(sys.argv[1], sep='\t', header='infer')
Value = Data.iloc[:, 2:]
Gene_length = len(Value.iloc[:, 1].tolist())
Value = Value.transpose()

result = pd.concat([Value[col] for col in Value.columns], ignore_index=True)
result = pd.DataFrame(result)
result.columns = ['Meth']
result['Group'] = (['CR'] * 12 + ['NR'] * 12) * Gene_length
result['Gene'] = [gene for gene in Data.iloc[:,3] for _ in range(42)]

result.to_csv(sys.argv[2], sep='\t', index=False, header='infer')