#!/usr/bin/python3

import sys
import os
import pandas as pd
import argparse
from itertools import chain
import glob
#-----------------------------------------------------------#
parser = argparse.ArgumentParser(description="Code Usage")
parser.add_argument("1", metavar="<Sample Group and number>", nargs="+", help='Write Sample Group and name. ex)A 12 B 12 ...')
args=parser.parse_args()
#-----------------------------------------------------------#
Info = sys.argv[1:]
group = Info[0::2]
number = Info[1::2]

Group = [list(map(lambda num: f'{gp}_{num}', list(range(1, int(num)+1)))) for num, gp in zip(number, group)]
Group = list(chain(*Group))
#-----------------------------------------------------------#
file_list = glob.glob('*cov')
file_list.sort()

Matching = dict(zip(file_list, Group))
Table = pd.Series(Matching)
Table = pd.DataFrame(Table)
Table = Table.reset_index()
Table.columns = ['Sample Code' ,'Patient name']
Table.to_excel('../Results/Information.xlsx', sheet_name='Sample Info', index=False, header=True)
#-----------------------------------------------------------#
def rename(File):
    command = f'mv {File} {Matching[File]}.cov'
    os.system(command)

list(map(rename, file_list))
#-----------------------------------------------------------#