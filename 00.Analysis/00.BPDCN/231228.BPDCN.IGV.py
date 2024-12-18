import igv_remote
import os
import glob
import pandas as pd
#--------------------------------------------------------------------------------------#
Sample = glob.glob('*.results.xlsx')
Sample.sort()
Sample = [sample.split('.')[0] for sample in Sample]
#--------------------------------------------------------------------------------------#
for sample in Sample:
    if os.path.isdir(f'{sample}_IGV'):
        pass
    else:
        command = f'mkdir {sample}_IGV'
        os.system(command)

    Result = pd.read_excel(f'{sample}.results.xlsx', 
                           engine='openpyxl',
                           sheet_name='Pathogenic.VUS')
    Result = Result[Result['main.accession'] == 'O']
    Result = Result.dropna(subset=['Tier'])
    Result = Result.dropna(subset=['exon'])

    if Result.empty:
        continue
    else:
        ir = igv_remote.IGV_remote()
        ir.connect()
        ir.load(f'/media/run/01.BPDCN/{sample}/{sample}.Real.bam')

        for row in range(Result.shape[0]):
            Tier = Result.iloc[row, 2]
            Position = Result.iloc[row, 4]
            Splitted = Position.split(':')
            Chr = str(Splitted[0])
            Start = int(Splitted[1].split('-')[0])
            End = int(Splitted[1].split('-')[1])
            Start_modified = Start - 15
            End_modified = End + 15
            Gene = Result.iloc[row, 5]
            Variant = Result.iloc[row, 8]
            Variant = Variant.replace('>','_')
            Variant = Variant.replace('*','_')
            Canonical = Result.iloc[row, 10]
            VAF = Result.iloc[row, 13]

            ir.set_saveopts(img_dir = f'{sample}_IGV/', img_basename = f'{sample}.{Chr}.{str(Start)}.{str(End)}.{Gene}.{Variant}.{Canonical}.{VAF}.png')
            ir.goto(Chr, Start, End)
            ir.snapshot()

        ir.new()
        ir.close()