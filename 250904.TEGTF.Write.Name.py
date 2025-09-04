import os
import sys
#-------------------------------------------#
# Version = ['hg19', 'hg38']
Version = ['hg19']

for ver in Version:
    File = f"/media/src/DB/{ver}/01.GTF/99.BackUp/gencode.{ver}.TE.gtf"
    with open(f"{File.replace('TE.gtf', 'TE.re.gtf')}", 'w') as note_te:
        with open(File, 'r') as gtf:
            for line in gtf:
                line = line.strip()
                if line.startswith('chr'):
                    line = line[3:]
                Info = line.split('\t')[8].split(';')[3].strip()
                Type = Info.split(' ')[1].strip()
                NEW_1 = f" gene_type {Type}"
                NEW_2 = f"; transcript_type {Type};"
                New_line = line + NEW_1 + NEW_2
                note_te.write(New_line + '\n')