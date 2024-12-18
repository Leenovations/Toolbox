#!/usr/bin/python3

import pandas as pd
import argparse
import glob
#----------------------------------------------------------------#
# parser = argparse.ArgumentParser(description='Code Usage')
# parser.add_argument('1', metavar='<File Path>', help='Set File Path')
# args = parser.parse_args()
#----------------------------------------------------------------#
Files = glob.glob('*.structural.flt.DEL.results.xlsx')
Files.sort()
Files = Files
ID = ['BPDCN' + str(index) for index in range(1, 14)]
Matching = dict(zip(Files, ID))
#----------------------------------------------------------------#
Total = []
Count = []
def Table(sample):
    Data = pd.read_excel(sample,
                         engine='openpyxl',
                         header='infer',
                         sheet_name='Sheet1')

    Flt = Data[['Type', 'Target']]
    DICT = {}
    for row in range(Flt.shape[0]):
        if Flt.iloc[row, 1] not in DICT.keys():
            DICT[Flt.iloc[row, 1]] = Flt.iloc[row, 0]
        elif Flt.iloc[row, 1] in DICT.keys():
            DICT[Flt.iloc[row, 1]] += ', ' + Flt.iloc[row, 0]

    df = pd.DataFrame({Matching[sample] : DICT.values()},
                      index=DICT.keys())
    
    df2 = pd.DataFrame({Matching[sample] : [len(value.split(', ')) for value in DICT.values()]},
                       index=DICT.keys())

    df.to_excel(Matching[sample] + '.DEL.xlsx',
                engine='openpyxl',
                sheet_name='Deletion',
                index='infer')
    
    Total.append(df)
    Count.append(df2)
    
list(map(Table, Files))
#----------------------------------------------------------------#
Merged = pd.concat(Total, axis=1)
Count = pd.concat(Count, axis=1)
#----------------------------------------------------------------#
excel_writer = pd.ExcelWriter('Total.DEL.DUP.Count.xlsx')

Merged.to_excel(excel_writer,
                engine='openpyxl',
                sheet_name='Variation',
                index='infer')

Count.to_excel(excel_writer,
               engine='openpyxl',
               sheet_name='Count',
               index='infer')

excel_writer.close()