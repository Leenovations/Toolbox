import pandas as pd
#------------------------------------------------------------------------------------------#
with open('/media/src/hg19/08.bed/Refseq.Curated.bed', 'r') as refseq:
    with open('/media/src/hg19/08.bed/Refseq.Curated.GeneCNV.Exon.bed', 'w') as note01:
        for line in refseq:
            if line.startswith('#'):
                continue
            line = line.strip()
            splitted = line.split('\t')
            NM = splitted[0]
            Chr = splitted[1]
            Strand = splitted[2]
            Count = int(splitted[3])
            ExonStart_list = splitted[4].split(',')
            ExonEnd_list = splitted[5].split(',')
            GeneSymbol = splitted[6]

            for ct in range(0, Count):
                note01.write(Chr + '\t' + ExonStart_list[ct] + '\t' + ExonEnd_list[ct] + '\t' + GeneSymbol + '\t' + NM + '\n')