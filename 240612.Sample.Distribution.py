import pandas as pd
import os
from string import ascii_uppercase
#----------------------------------------------------------#
Sample_Data = pd.read_csv('/media/node04-HDD01/01.Gleevec/Total.txt',
                          sep='\t',
                          header=None,
                          names=['Sample'])
#----------------------------------------------------------#
Start = 0
DIR_Count = 1
for row in range(10, Sample_Data.shape[0] + 10, 10):
    Subset = Sample_Data.iloc[Start:row, ]
    Start += 10
    os.makedirs(str(DIR_Count), exist_ok=True)

    Fastq_list = Subset['Sample'].to_list()

    SAMPLE = []
    R_1 = []
    R_2 = []
    MB = []
    for fq in Fastq_list[0::2]:
        Sample_name = fq.split('/')[-1].split('_R1_')[0]
        os.makedirs(f'{DIR_Count}/{Sample_name}', exist_ok=True)
        R1 = fq
        R2 = fq.replace('R1', 'R2')
        SAMPLE.append(Sample_name)
        R_1.append(R1)
        R_2.append(R2)
        MB.append('2 MB')

        Completed_df = pd.DataFrame({'Sample' : Sample_name,
                            'R1' : R1,
                            'R2' : R2,
                            'MB' : MB})
        Completed_df.to_csv(f'{DIR_Count}/{Sample_name}/SampleSheet.txt',
                    sep='\t',
                    header=None,
                    index=False)

    Completed_df = pd.DataFrame({'Sample' : SAMPLE,
                                 'R1' : R_1,
                                 'R2' : R_2,
                                 'MB' :MB})
    Completed_df.to_csv(f'{DIR_Count}/SampleSheet.txt',
                        sep='\t',
                        header=None,
                        index=False)
    DIR_Count += 1