import sys
#--------------------------------------------------------#
with open(sys.argv[1], 'r') as gtf:
    with open(sys.argv[2], 'w') as note:
        note.write('ID' + '\t' + 'Type' + '\t' + 'GeneSymbol' + '\t' + 'Length' + '\n')
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
                    Info = splitted[8].split(';')
                    ID = Info[0].split('"')[1]
                    Type = Info[2].split('"')[1]
                    GeneSymbol = Info[4].split('"')[1]
                    note.write(ID + '\t' + GeneSymbol + '\t' + Type + '\t' + length + '\n')