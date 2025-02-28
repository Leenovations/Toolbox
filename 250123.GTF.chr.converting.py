# with open('/media/DB/gencode.v47lift37.annotation.gtf', 'r') as gtf:
#     with open('/media/DB/Gencode.hg19.v37.gtf', 'w') as note00:
#         for line in gtf:
#             if line.startswith('#'):
#                 note00.write(line)
#             else:
#                 line = line.strip()
#                 splitted = line.split('\t')
#                 if splitted[0].startswith('chrM'):
#                     splitted[0] = splitted[0].replace('chrM', 'MT')
#                 elif splitted[0].startswith('chr'):
#                     splitted[0] = splitted[0].replace('chr', '')
#                 line = '\t'.join(splitted)
#                 note00.write(line + '\n')

with open('/media/DB/hg19/00.FASTA/test.fasta', 'r') as fa:
    with open('/media/DB/hg19/00.FASTA/modified.fasta', 'w') as note00:
        for line in fa:
            if line.startswith('>'):
                Chr = line.split(' ')[0]
                note00.write(Chr + '\n')
            else:
                note00.write(line)