#!/home/lab/anaconda3/envs/NGS/bin/python3

import sys
import argparse
#--------------------------------------------------------------------#
parser = argparse.ArgumentParser(description="Pipeline Usage")
parser.add_argument('1', metavar='<window size>', help='Set window size')
args = parser.parse_args()
#--------------------------------------------------------------------#
GENE = {}
with open('/media/src/hg19/01.Methylation/00.Bed/NCBI.RefSeq.Selected.Gene.bed', 'r') as txt:
    for line in txt:
        line = line.strip()
        splitted = line.split('\t')
        Chr = splitted[0]
        Start = splitted[1]
        End = splitted[2]
        Gene = splitted[3]
        Strand = splitted[4]
        
        if Chr != 'M' and Chr != 'chrM':
            GENE[Gene] = Chr + '\t' + Start + '\t' + End + '\t' + Strand
#--------------------------------------------------------------------#
with open(f"/media/src/hg19/01.Methylation/00.Bed/NCBI.RefSeq.Selected.Gene.{str(sys.argv[1])}bp.bed", 'w') as note:
    for gene in GENE.keys():
        Chr = GENE[gene].split('\t')[0]
        Start = int(GENE[gene].split('\t')[1])
        End = Start + int(sys.argv[1])
        Strand = GENE[gene].split('\t')[3]
        note.write(Chr + '\t' + str(Start) + '\t' + str(End) + '\t' + gene + '\t' +Strand + '\n')
        End_point = int(GENE[gene].split('\t')[2])
        while End_point > End :
            Start = End + 1
            End += int(sys.argv[1]) + 1

            if End >= End_point:
                note.write(Chr + '\t' + str(Start) + '\t' + str(End_point) + '\t' + gene + '\t' +Strand + '\n')
                break
            else:
                note.write(Chr + '\t' + str(Start) + '\t' + str(End) + '\t' + gene + '\t' +Strand + '\n')
#--------------------------------------------------------------------#
with open(f"/media/src/hg19/01.Methylation/00.Bed/NCBI.RefSeq.Selected.Gene.{str(sys.argv[1])}bp.bed", 'r') as bed:
    with open(f"/media/src/hg19/01.Methylation/00.Bed/NCBI.RefSeq.Selected.Gene.{str(sys.argv[1])}bp.Chr.X.bed", 'w') as note:
        for line in bed:
            line = line.replace('chr', '')
            note.write(line)
#--------------------------------------------------------------------#