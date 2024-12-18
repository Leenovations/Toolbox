#!/home/lab/anaconda3/envs/NGS/bin/python3

import sys
import argparse
#--------------------------------------------------------------------#
parser = argparse.ArgumentParser(description="Pipeline Usage")
parser.add_argument('1', metavar='<window size>', help='Set window size')
args = parser.parse_args()
#--------------------------------------------------------------------#
Chromosome_Length = {}
with open('/media/src/hg19/00.RNA/Index/chrNameLength.txt', 'r') as txt:
    for line in txt:
        line = line.strip()
        splitted = line.split('\t')
        Chr = splitted[0]
        Length = splitted[1]
        
        if Chr.startswith('chr') and Chr != 'M' and Chr != 'chrM':
            Chromosome_Length[Chr] = Length
#--------------------------------------------------------------------#
with open(f"/media/src/hg19/01.Methylation/00.Bed/{str(sys.argv[1])}bp.bed", 'w') as note:
    Start = 1
    End = int(sys.argv[1])
    for chromosome in Chromosome_Length.keys():
        note.write(chromosome + '\t' + str(Start) + '\t' + str(End) + '\n')
        End_point = int(Chromosome_Length[chromosome])
        while End_point > End :
            Start += int(sys.argv[1])
            End += int(sys.argv[1])

            if End >= End_point:
                note.write(chromosome + '\t' + str(Start) + '\t' + str(End_point) + '\n')
                Start = 1
                End = int(sys.argv[1])
                break
            else:
                note.write(chromosome + '\t' + str(Start) + '\t' + str(End) + '\n')
#--------------------------------------------------------------------#
with open(f"/media/src/hg19/01.Methylation/00.Bed/{str(sys.argv[1])}bp.bed", 'r') as bed:
    with open(f"/media/src/hg19/01.Methylation/00.Bed/{str(sys.argv[1])}bp.Chr.X.bed", 'w') as note:
        for line in bed:
            line = line.replace('chr', '')
            note.write(line)
#--------------------------------------------------------------------#