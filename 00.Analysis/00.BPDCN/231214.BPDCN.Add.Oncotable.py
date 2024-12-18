#!/usr/bin/python3

import pandas as pd
import sys
import glob
import argparse
#-----------------------------------------------------------------#
Onco_Input = pd.read_excel('231205.BPDCN.Onco.InPut.xlsx',
                           header=0,
                           sheet_name='Sheet1')

ID = pd.read_excel('231205.BPDCN.Onco.InPut.xlsx',
                           header=0,
                           sheet_name='Sheet2')

CNV  = pd.read_excel('BPDCN.CNV.xlsx',
                   header=None,
                   sheet_name='CNV')

CNV[2] = CNV[2].replace('DEL', 'Deletion')
CNV[2] = CNV[2].replace('DUP', 'Amplification')
#-----------------------------------------------------------------#
Matching = dict(zip(ID['Sample'], ID['ID']))
#-----------------------------------------------------------------#
for row in range(0, CNV.shape[0]):
    Gene = CNV[15][row]
    Variation = CNV[2][row]
    Sample = Matching[CNV[0][row]]

    target = Onco_Input[Onco_Input['Gene'] == Gene].index
    if not target.empty:
        target_row_index = target[0]
        current_value = Onco_Input.at[target_row_index, f'{Sample}']
        
        if isinstance(current_value, str) and current_value.strip() != '':
            Onco_Input.at[target_row_index, f'{Sample}'] = current_value + '; ' + Variation
        else:
            Onco_Input.at[target_row_index, f'{Sample}'] = Variation

    else:
        new_row = pd.DataFrame.from_dict([{'Gene' : Gene, f'{Sample}' : Variation}])
        Onco_Input = pd.concat([Onco_Input, new_row], ignore_index=True)



NA_Count = Onco_Input.isna().sum(axis=1)
Onco_Input = Onco_Input[NA_Count != 13]

print(Onco_Input)

Onco_Input.to_excel(excel_writer='231205.BPDCN.Oncoprint.xlsx',
                    sheet_name='OncoPrint',
                    header='infer',
                    index=False)
