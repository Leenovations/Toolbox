import os
import sys
#------------------------------------------------------------------------#
OutVCF = sys.argv[1].replace('vcf', 'sorted.vcf')
command = f'grep "^#" {sys.argv[1]} > {OutVCF}'
os.system(command)
command = f'grep -v "^#" {sys.argv[1]} | sort -k1,1V -k2n >> {OutVCF}'
os.system(command)
#------------------------------------------------------------------------#