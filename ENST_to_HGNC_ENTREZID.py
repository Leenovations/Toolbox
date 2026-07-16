import pandas as pd
import sys
#python3 sys.argv[0] hg19/hg38
#--------------------------------------------#
HGNC = pd.read_csv(f"/media/src/DB/{sys.argv[1]}/01.GTF/gencode.{sys.argv[1]}.HGNC.txt", sep='\t', header=None)
HGNC.columns = ['ENST', 'GeneSymbol', 'HGNC']

ENTREZ = pd.read_csv(f"/media/src/DB/{sys.argv[1]}/01.GTF/gencode.{sys.argv[1]}.EntrezGene.txt", sep='\t', header=None)
ENTREZ.columns = ['ENST', 'ENTREZ']

Merged = pd.merge(HGNC, ENTREZ, how='inner', on='ENST')
Merged.dropna(inplace=True)
Merged = Merged[['GeneSymbol', 'ENTREZ']]
Merged = Merged.drop_duplicates()

Merged.to_csv(f"/media/src/DB/{sys.argv[1]}/01.GTF/gencode.{sys.argv[1]}.Symbol.ENTREZ.txt", sep='\t', index=False, header='infer')