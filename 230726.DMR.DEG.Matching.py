#!/usr/bin/python3

import openpyxl
import pandas as pd 

def Merge_data(Region:str):
    if Region == 'Promoter_DMR':
        DEG = pd.read_excel('/labmed/00.Code/00.Methylation/08.Table/230625.AML.Total.Data.xlsx', sheet_name = 'DEG')
        DMR = pd.read_excel('/labmed/00.Code/00.Methylation/08.Table/230625.AML.Total.Data.xlsx', sheet_name = Region)

        Expression = DEG[['gene_id','DEG']]
        Methylation = DMR[['Gene','Direction']]

        Expression.columns = ['Gene','DEG']
        Methylation.columns = ['Gene', 'DMR']

        Merge = pd.merge(Expression, Methylation, how='outer', on='Gene')
        Merge = Merge.dropna()

        Merge['Match'] = Merge.apply(lambda row: 'O' if (row['DEG'] == 'Responsive' and row['DMR'] == 'hyper') or \
                                             (row['DEG'] == 'Unresponsive' and row['DMR'] == 'hypo') \
                                    else '∆' if (row['DEG'] == 'Responsive' and row['DMR'] == 'hypo') or \
                                             (row['DEG'] == 'Unresponsive' and row['DMR'] == 'hyper') \
                                    else 'X', axis=1)

        custom_order = {'O': 1, '∆': 2, 'X': 3}
        Merge['Match'] = Merge['Match'].map(custom_order)
        Merge = Merge.sort_values(by='Match')

        custom_order = {1:'O', 2:'∆', 3:'X'}
        Merge['Match'] = Merge['Match'].map(custom_order) 
        return Merge
    
    else:
        DEG = pd.read_excel('/labmed/00.Code/00.Methylation/08.Table/230625.AML.Total.Data.xlsx', sheet_name = 'DEG')
        DMR = pd.read_excel('/labmed/00.Code/00.Methylation/08.Table/230625.AML.Total.Data.xlsx', sheet_name = Region)

        Expression = DEG[['gene_id','DEG']]
        Methylation = DMR[['annot.symbol','DM_status']]

        Expression.columns = ['Gene','DEG']
        Methylation.columns = ['Gene', 'DMR']

        Merge = pd.merge(Expression, Methylation, how='outer', on='Gene')
        Merge = Merge.dropna()

        Merge['Match'] = Merge.apply(lambda row: 'O' if (row['DEG'] == 'Responsive' and row['DMR'] == 'hyper') or \
                                             (row['DEG'] == 'Unresponsive' and row['DMR'] == 'hypo') \
                                    else '∆' if (row['DEG'] == 'Responsive' and row['DMR'] == 'hypo') or \
                                             (row['DEG'] == 'Unresponsive' and row['DMR'] == 'hyper') \
                                    else 'X', axis=1)

        custom_order = {'O': 1, '∆': 2, 'X': 3}
        Merge['Match'] = Merge['Match'].map(custom_order)
        Merge = Merge.sort_values(by='Match')

        custom_order = {1:'O', 2:'∆', 3:'X'}
        Merge['Match'] = Merge['Match'].map(custom_order)   

        return Merge


def draw_color_at_nan(row):
    if row['Match'] == 'O':
        return ['background-color: #ffff90'] * len(row)
    elif row['Match'] == '∆':
        return ['background-color: #bdffa8'] * len(row)
    else:
        return [''] * len(row)
    
Data = pd.ExcelWriter('230726.DMR.DEG.Matching.xlsx', engine='openpyxl')

promoter = Merge_data('Promoter_DMR')
promoter = promoter.style.apply(draw_color_at_nan, axis=1)
promoter.to_excel(Data, sheet_name='Promoter', index=False)

exon = Merge_data('Exon_DMR')
exon = exon.style.apply(draw_color_at_nan, axis=1)
exon.to_excel(Data, sheet_name='Exon', index=False)

exon = Merge_data('Intron_DMR')
exon = exon.style.apply(draw_color_at_nan, axis=1)
exon.to_excel(Data, sheet_name='Intron', index=False)

Data.save()