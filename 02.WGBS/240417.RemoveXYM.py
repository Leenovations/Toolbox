#!/usr/bin/python3

import glob
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor
#-------------------------------------------------------------------
# Files = glob.glob('/labmed/02.AML/08.GSE163522/01.BismarkCov/SRR1745468*.bismark.cov')
Files = glob.glob('/labmed/02.AML/00.Input/Figure1F/*xym*')
#-------------------------------------------------------------------
def Cal(cpg_file):
    Chromosome = [str(num) for num in range(1,23)]
    Prefix = cpg_file.split('/')[-1]
    Prefix = Prefix.split('.')[0]
    with open(f'/labmed/02.AML/00.Input/Figure1F/{Prefix}.cov.tsv', 'w') as note01:
        with open(cpg_file, 'r') as cpg:
            for line in cpg:
                line = line.strip()
                splitted = line.split('\t')
                Chr = splitted[0]
                if Chr in Chromosome:
                    note01.write(line + '\n')
                else:
                    continue

if __name__ == '__main__':
    num_threads = 2
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(Cal, Files)
#-------------------------------------------------------------------#