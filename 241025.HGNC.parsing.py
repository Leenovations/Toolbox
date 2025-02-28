import pandas as pd
#------------------------------------------------------------#
Data = pd.read_csv('/media/src/Classification/hgnc_complete_set_2024-10-01.txt', sep='\t', header='infer', low_memory=False)
Data = Data[['hgnc_id', 'symbol', 'name', 'location', 'alias_symbol', 'ensembl_gene_id', 'ucsc_id', 'vega_id', 'refseq_accession', 'uniprot_ids', 'mane_select']]
Data['mane_select'].fillna('None|None', inplace=True)
Data[['mane_ensembl', 'mane_refseq']] = Data['mane_select'].str.split('|', expand=True,)
Data = Data[['hgnc_id', 'symbol', 'mane_ensembl', 'mane_refseq', 'name', 'location', 'alias_symbol', 'ensembl_gene_id', 'ucsc_id', 'vega_id', 'refseq_accession', 'uniprot_ids']]
Data.to_csv('HGNC_data.tsv', sep='\t', index=False)