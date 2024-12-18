#!/home/lab/anaconda3/envs/NGS/bin/python3

import pandas as pd
import os
#------------------------------------------------------------#
with open("/media/src/hg19/08.bed/NCBI.RefSeq.Selected.Exon.Chr.X.bed", "r") as bed:
    with open("/media/src/hg19/08.bed/NCBI.RefSeq.Selected.GeneCNV.Chr.X.bed", "w") as note:
        for line in bed:
            line = line.strip()
            splitted = line.split('\t')
            Chr = splitted[0]
            Start = int(splitted[1])
            End = int(splitted[2])
            Gene = splitted[3]
            Exon = splitted[4]
            Strand = splitted[5]

            for position in range(Start, End + 1):
                note.write(Chr + '\t' + str(position - 1) + '\t' + str(position + 1) + '\t' + Gene + '\t' + Exon + '\t' + Strand + '\n')

Exon = pd.read_csv(f"/media/src/hg19/08.bed/NCBI.RefSeq.Selected.GeneCNV.Chr.X.bed",
                sep='\t',
                low_memory=False,
                header=None)
Gene = list(set(Exon.iloc[:, 3].to_list()))

for gene in Gene:
	if os.path.isfile(f"/media/src/hg19/04.cnv/{gene}.cnv.bed"):
		continue
	else:
		Bed = Exon[Exon.iloc[:, 3] == gene]
		Bed.to_csv(f"/media/src/hg19/04.cnv/{gene}.cnv.bed",
				sep='\t',
				index=False,
				header=None)
