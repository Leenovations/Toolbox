import pandas as pd
import sys
#----------------------------------------------------------------------#
Germline = sys.argv[1]
Somatic = sys.argv[2]
#----------------------------------------------------------------------#
Germline_vcf = pd.read_csv(Germline, sep='\t', comment='#', header=None, low_memory=False)
Somatic_vcf = pd.read_csv(Somatic, sep='\t', comment='#', header=None, low_memory=False)

Germline_vcf = Germline_vcf.iloc[:, :2]
Somatic_vcf = Somatic_vcf.iloc[:, :2]
#----------------------------------------------------------------------#
Merged = pd.merge(Germline_vcf, Somatic_vcf, on=[0, 1])
Merged.to_csv('Mutation_position_v2.tsv', sep='\t', index=False, header=None)