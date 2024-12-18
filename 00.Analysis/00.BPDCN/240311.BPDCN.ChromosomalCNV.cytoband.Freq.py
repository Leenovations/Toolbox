AMP_COUNT = {}
DEL_COUNT = {}
Chromosome = ['chr' + str(i) for i in range(1,23)] + ['chrX', 'chrY']
CHROMOSOME = {Chr: 0 for Chr in Chromosome}

with open('/labmed/06.BPDCN/BPDCN.ChromosomalCNV.Cytoband.txt', 'r') as cyto:
    for i,line in enumerate(cyto):
        VALUE = []
        line = line.strip()
        splitted = line.split('\t')
        Position = splitted[0] + '.' + splitted[3]
        Chromosome = splitted[0]
        if len(splitted[4:]) > 0:
            for val in splitted[4:]:
                if ',' in val:
                    two = val.split(',')
                    for t in two:
                        t = t.strip()
                        VALUE.append(t)
                elif val == 'AMP':
                    VALUE.append(val)
                elif val == 'DEL':
                    VALUE.append(val)

        AMP = VALUE.count('AMP')
        if AMP != 0:
            AMP_COUNT[Position] = AMP
            CHROMOSOME[Chromosome] += AMP

        DEL = VALUE.count('DEL')
        if DEL != 0:
            DEL_COUNT[Position] = DEL
            CHROMOSOME[Chromosome] += DEL

with open('/labmed/06.BPDCN/BPDCN.ChromosomalCNV.Cytoband.Freq.input.txt', 'w') as note:
    note.write('locus' + '\t' + 'Freq' + '\t' + 'Type' + '\n')
    for amp in AMP_COUNT.keys():
        note.write(amp + '\t' + str(AMP_COUNT[amp]) + '\t' + 'Gain' + '\n')
    
    for Del in DEL_COUNT.keys():
        note.write(Del + '\t' + str(DEL_COUNT[Del]) + '\t' + 'Loss' + '\n')

with open('/labmed/06.BPDCN/BPDCN.ChromosomalCNV.CHR.Freq.input.txt', 'w') as note:
    note.write('locus' + '\t' + 'Freq' + '\n')
    for Chr in CHROMOSOME.keys():
        note.write(Chr + '\t' + str(CHROMOSOME[Chr]) + '\n')