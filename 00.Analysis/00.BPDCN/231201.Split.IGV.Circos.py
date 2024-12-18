#!/usr/bin/python3

import sys
import argparse
import re
#-------------------------------------------------------------#
parser = argparse.ArgumentParser(description='Code Usage')
parser.add_argument('1', metavar='<IGV bed>', help='Set IGV bed file')
parser.add_argument('2', metavar='<Prefix>', help='Set output name')
args = parser.parse_args()
#-------------------------------------------------------------#
with open(sys.argv[2] + '.link.bed', 'w') as note:
    with open(sys.argv[1], 'r') as bed:
        for line in bed:
            line = line.strip()
            line = line.replace('chr', 'hs')
            splitted = re.split(r'[-\s;:]', line)
            splitted = splitted[2:]
            joined = '\t'.join(splitted)

            note.write(joined + '\n')

#-------------------------------------------------------------#
with open(sys.argv[2] + '.gene.bed', 'w') as note:
    with open(sys.argv[1], 'r') as bed:
        for line in bed:
            line = line.strip()
            line = line.replace('chr', 'hs')
            splitted = re.split(r'[-\s;:\t]', line)
            # print(splitted)

            note.write('\t'.join(splitted[2:5]) + '\t' + splitted[0] + '\n' + '\t'.join(splitted[5:]) + '\t' + splitted[1] + '\n')