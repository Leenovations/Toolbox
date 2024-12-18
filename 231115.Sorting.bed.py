#!/usr/bin/python3

import pandas as pd
import argparse
import sys
#--------------------------------------------------------------------#
parser = argparse.ArgumentParser(description="Code Usage \ File must have no header")
parser.add_argument("1", metavar="<bed>", help='Select bed file')
parser.add_argument("2", metavar="<column>", help='Select column number. ex) 0,1,2')
parser.add_argument("3", metavar="<Output name>", help='Set output name')
args=parser.parse_args()
#--------------------------------------------------------------------#
Data = pd.read_csv(sys.argv[1],
                   sep='\t',
                   header=None)
#--------------------------------------------------------------------#
Col_number = [int(idx) for idx in sys.argv[2].split(',')]
Data = Data.sort_values(Col_number)
#--------------------------------------------------------------------#
Data.to_csv(sys.argv[3],
            sep='\t',
            index=False,
            header=None)
#--------------------------------------------------------------------#
