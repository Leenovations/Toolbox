#!/usr/bin/python3

import pandas as pd
import glob
import concurrent.futures
#------------------------------------------------------------------------#
Coverage = glob.glob('Results/01.Normalized/*txt')
Coverage.sort()
#------------------------------------------------------------------------#
def trimming(Cov):
    Header = Cov.split('/')[-1]
    Header = Header.split('.')[0]

    Data = pd.read_csv(Cov, 
                       sep='\t', 
                       names = ['Chromosome','Start','End','Strand','T','C','U'],
                       dtype={'5': int, '4':int})

    Data[Header] = round(Data.iloc[0:,5] / Data.iloc[0:,4] * 100, 2)
    Data = Data.drop(['Strand','T','C','U'], axis=1)

    Data.to_csv(f'CpG/01.Trim/{Header}.trim.cov',
                sep='\t',
                header=True,
                index=False)

if __name__ == '__main__':
    num_threads = len(Coverage)
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(trimming, Coverage)
#------------------------------------------------------------------------#