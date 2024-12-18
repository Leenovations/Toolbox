#!/usr/bin/python3
#---------------------------------------------------------------------------------#
'''
This code is designed to generate a BED file by extracting specific information from the NCBI All Refseq Gene prediction file through Custom selection in the UCSC Table Browser. 
The selected information includes chromosome, strand, transcription start site (TxStart), transcription end site (TxEnd), start position of coding sequence (CDSStart), end position of coding sequence (CDSEnd), exon count, exon start positions, exon end positions, and gene symbol. 
The code divides the genomic regions for each gene, providing a structured BED file.
'''
#---------------------------------------------------------------------------------#
with open('/media/src/hg19/01.Methylation/00.Bed/NCBI.Ref.seq.bed', 'r') as ref:
    with open('/media/src/hg19/01.Methylation/00.Bed/NCBI.All.RefSeq.Gene.Annotation.bed', 'w') as note:
        for line in ref:
            line = line.strip()
            splitted = line.split('\t')
            ID = splitted[0]
            Chromosome = splitted[1]
            Strand = splitted[2]
            TxStart = splitted[3]
            TxEnd = splitted[4]
            CdsStart = splitted[5]
            CdsEnd = splitted[6]
            ExonCount = splitted[7]
            ExonStart = splitted[8]
            ExonStart = ExonStart.split(',')
            ExonEnd = splitted[9]
            ExonEnd = ExonEnd.split(',')
            GeneSymbol = splitted[10]

            if Strand =='+':
                Promoter = [Chromosome, str(int(TxStart) - 2001), str(int(TxStart) -1), GeneSymbol, 'Promoter', ID, Strand]
                Promoter = '\t'.join(Promoter)
                note.write(Promoter + '\n')
                #------------------------------------------------#
                if int(TxStart) - int(CdsStart) == 0:
                    continue
                else:
                    UTR5 = [Chromosome, str(int(TxStart)), str(int(CdsStart) -1), GeneSymbol, '5UTR', ID, Strand]
                    UTR5 = '\t'.join(UTR5)
                    note.write(UTR5 + '\n')
                #------------------------------------------------#
                for num in range(int(ExonCount)):
                    Region = 'Exon' + f'_{num}'
                    Exon = [Chromosome, str(int(ExonStart[num])), str(int(ExonEnd[num])), GeneSymbol, Region, ID, Strand]
                    Exon = '\t'.join(Exon)
                    note.write(Exon + '\n')
                #------------------------------------------------#
                for num in range(int(ExonCount)):
                    if num == int(ExonCount) - 1:
                        continue
                    Region = 'Intron' + f'_{num}'
                    Intron = [Chromosome, str(int(ExonEnd[num]) + 1), str(int(ExonStart[num+1]) - 1), GeneSymbol, Region, ID, Strand]
                    Intron = '\t'.join(Intron)
                    note.write(Intron + '\n')
                #------------------------------------------------#
                if int(TxEnd) - int(CdsEnd) == 0:
                    continue
                else:
                    UTR3 = [Chromosome, str(int(CdsEnd) + 1), str(int(TxEnd)), GeneSymbol, '3UTR', ID, Strand]
                    UTR3 = '\t'.join(UTR3)
                    note.write(UTR3 + '\n')
                #------------------------------------------------#

            elif Strand =='-':
                Promoter = [Chromosome, str(int(TxEnd) + 1), str(int(TxEnd) + 2001), GeneSymbol, 'Promoter', ID, Strand]
                Promoter = '\t'.join(Promoter)
                note.write(Promoter + '\n')
                #------------------------------------------------#
                if int(TxEnd) - int(CdsEnd) == 0:
                    continue
                else:
                    UTR5 = [Chromosome, str(int(CdsEnd) + 1), str(int(TxEnd)), GeneSymbol, 'UTR5', ID, Strand]
                    UTR5 = '\t'.join(UTR5)
                    note.write(UTR5 + '\n')
                #------------------------------------------------#
                for num in reversed(range(int(ExonCount))):
                    Region = 'Exon' + f'_{int(ExonCount) - num - 1}'
                    Exon = [Chromosome, str(int(ExonStart[num])), str(int(ExonEnd[num])), GeneSymbol, Region, ID, Strand]
                    Exon = '\t'.join(Exon)
                    note.write(Exon + '\n')
                #------------------------------------------------#
                for num in reversed(range(int(ExonCount))):
                    if num == 0:
                        continue
                    Region = 'Intron' + f'_{int(ExonCount) - num - 1}'
                    Intron = [Chromosome, str(int(ExonEnd[num-1]) + 1), str(int(ExonStart[num]) - 1), GeneSymbol, Region, ID, Strand]
                    Intron = '\t'.join(Intron)
                    note.write(Intron + '\n')
                #------------------------------------------------#
                if int(TxStart) - int(CdsStart) == 0:
                    continue
                else:
                    UTR3 = [Chromosome, str(int(TxStart)), str(int(CdsStart) - 1), GeneSymbol, '3UTR', ID, Strand]
                    UTR3 = '\t'.join(UTR3)
                    note.write(UTR3 + '\n')
                #------------------------------------------------#