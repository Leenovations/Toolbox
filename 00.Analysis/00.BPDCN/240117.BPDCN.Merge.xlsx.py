import os
import glob
import pandas as pd
#--------------------------------------------------------------------------------------#
Sample = glob.glob('*.results.xlsx')
Sample.sort()
Sample = [sample.split('.')[0] for sample in Sample]
#--------------------------------------------------------------------------------------#
DICT = {'Name':[],
        'Position':[],
        'Gene':[],
        'Variant':[],
        'Canonical':[],
        'VAF':[]}

for sample in Sample:
    IGV = glob.glob(f"{sample}_IGV/*png")
    for igv in IGV:
        igv = igv.replace(f"{sample}_IGV/", '')
        splitted = igv.split('.')
        if len(splitted) < 11 :
            continue
        else:
            Name = splitted[0]
            Position = splitted[1] + ':' + splitted[2] + '-' + splitted[3]
            Gene = splitted[4]
            Variant = splitted[5] + splitted[6]
            Canonical = splitted[7]

            if 'del' in Variant and 'fs' in Canonical:
                DICT['Name'].append(Name)
                DICT['Position'].append(Position)
                DICT['Gene'].append(Gene)
                Canonical = 'Truncating'
                DICT['Variant'].append(Variant)
                DICT['Canonical'].append(Canonical)
                VAF = splitted[8] + '.' + splitted[9]
                VAF = VAF.split('_')[0]
                DICT['VAF'].append(VAF)
            elif 'dup' in Variant and 'fs' in Canonical:
                DICT['Name'].append(Name)
                DICT['Position'].append(Position)
                DICT['Gene'].append(Gene)
                Canonical = 'Truncating'
                DICT['Variant'].append(Variant)
                DICT['Canonical'].append(Canonical)
                VAF = splitted[8] + '.' + splitted[9]
                VAF = VAF.split('_')[0]
                DICT['VAF'].append(VAF)
            elif 'del' in Variant and 'nan' in Canonical:
                DICT['Name'].append(Name)
                DICT['Position'].append(Position)
                DICT['Gene'].append(Gene)
                Canonical = 'Deletion'
                DICT['Variant'].append(Variant)
                DICT['Canonical'].append(Canonical)
                VAF = splitted[8] + '.' + splitted[9]
                VAF = VAF.split('_')[0]
                DICT['VAF'].append(VAF)
            elif 'dup' in Variant and 'nan' in Canonical:
                DICT['Name'].append(Name)
                DICT['Position'].append(Position)
                DICT['Gene'].append(Gene)
                Canonical = 'Duplication'
                DICT['Variant'].append(Variant)
                DICT['Canonical'].append(Canonical)
                VAF = splitted[8] + '.' + splitted[9]
                VAF = VAF.split('_')[0]
                DICT['VAF'].append(VAF)
            elif '_' in Variant and 'nan' not in Canonical:
                DICT['Name'].append(Name)
                DICT['Position'].append(Position)
                DICT['Gene'].append(Gene)
                Canonical = 'Missense'
                DICT['Variant'].append(Variant)
                DICT['Canonical'].append(Canonical)
                VAF = splitted[8] + '.' + splitted[9]
                VAF = VAF.split('_')[0]
                DICT['VAF'].append(VAF)
            elif '_' in Variant and 'nan' in Canonical:
                continue

DICT = pd.DataFrame(DICT)
DICT.to_excel('BPDCN.Variant.Merge.xlsx',
              sheet_name='Variants',
              header='infer')