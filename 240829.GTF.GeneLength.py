import sys 
#--------------------------------------------------------#
with open(sys.argv[1], 'r') as gtf:
    with open(sys.argv[2], 'w') as note:
        note.write('ID' + '\t' + 'GeneSymbol' + '\t' + 'Type' + '\t' + 'Length' + '\n')
        for line in gtf:
            line = line.strip()
            if line.startswith('#'):
                continue
            else:
                splitted = line.split('\t')
                Gene = splitted[2]
                if Gene == 'gene':
                    Start = int(splitted[3])
                    End = int(splitted[4])
                    length = str(End - Start)
                    Info = splitted[8].split(';') #버전에 따라 Info 순서 다를 수 있음
                    ID = Info[0].split('"')[1] # GFF는 [1] GTF는 [0]
                    Type = Info[2].split('"')[1]
                    GeneSymbol = Info[1].split('"')[1].split('_')[0]
                    note.write(ID + '\t' + GeneSymbol + '\t' + Type + '\t' + length + '\n')