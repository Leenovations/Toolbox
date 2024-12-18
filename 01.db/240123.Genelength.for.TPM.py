import pandas as pd 

#---------------------------------------------------------------------------------#
with open('/media/src/hg19/00.RNA/hg19.GENCODE.v44.GeneLength.txt', 'w') as note:
    with open('/media/src/hg19/00.RNA/hg19.GENCODE.v44.annotation.gtf', 'r') as gtf:
        for line in gtf:
            line = line.strip()
            if line.startswith('#'):
                continue
            else:
                splitted = line.split('\t')
                Region = splitted[2]
                if Region == 'gene':
                    Start = splitted[3]
                    End = splitted[4]
                    Strand = splitted[6]
                    Info = splitted[8]
                    Length = str(int(End) - int(Start))
                    Description = Info.split(';')
                    Gene_ID = Description[0].split(' ')[1]
                    Gene_ID = Gene_ID.replace('"', '')

                    Gene_type = Description[1].split(' ')[2]
                    Gene_type = Gene_type.replace('"', '')

                    Gene_Symbol = Description[2].split(' ')[2]
                    Gene_Symbol = Gene_Symbol.replace('"', '')

                    note.write('\t'.join([Gene_ID, Gene_type, Gene_Symbol, Length]) + '\n')