#!/usr/bin/python3

import sys
import os
import time
import argparse
import pandas as pd
#----------------------------------------------------------------------------------------#
parser = argparse.ArgumentParser(description='Pipeline Usage')
parser.add_argument('1', metavar='<38 or 19>' ,help='Select Reference version')
args = parser.parse_args()
#----------------------------------------------------------------------------------------#
if os.path.isfile('/media/src/hg{}/hg{}.GENCODE.fa.fai'.format(sys.argv[1], sys.argv[1])):
    pass
else:
    command = 'samtools faidx /media/src/hg{}/hg{}.GENCODE.fa'.format(sys.argv[1], sys.argv[1])
    os.system(command)