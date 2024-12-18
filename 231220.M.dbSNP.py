#!/usr/bin/python3

import os
import time
import argparse
import sys
import pandas as pd
import numpy as np
from fpdf import FPDF
from datetime import datetime
#----------------------------------------------------------------------------------------#
parser = argparse.ArgumentParser(description='Pipeline Usage')
parser.add_argument('1', metavar='<db>' ,help='Set Reference database')
parser.add_argument('1', metavar='<Output>' ,help='Set Output name')
args = parser.parse_args()
#----------------------------------------------------------------------------------------#
with open(sys.argv[2], 'w') as note:
    with open(sys.argv[1], 'r') as db:
        for line in db:
            line = line.strip()
            if line.startswith('##contig='):
                continue
            elif line.startswith('#'):
                note.write(line + '\n')
            else:
                if line.startswith('MT'):
                    line = line.replace('MT', 'M')
                    line = 'chr' + line
                    note.write(line + '\n')
                else:
                    line = 'chr' + line
                    note.write(line + '\n')
