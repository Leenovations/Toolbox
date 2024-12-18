#!/usr/bin/python3
import sys
import os
#-----------------------------------------------------------------------------------------#
Class = sys.argv[1]
LIST = sys.argv[2:]
#-----------------------------------------------------------------------------------------#
if len(LIST) % 2 == 0:
	pass
elif 'bam' in LIST[0]:
	pass
else:
	raise ValueError("\033[91mThe number of raw data files is odd\033[0m")
#-----------------------------------------------------------------------------------------#
with open(f'Datalist.{Class}.txt', 'w') as note2:
	for data in LIST:
		note2.write(data + '\n')
#-----------------------------------------------------------------------------------------#
with open(f'SampleSheet.{Class}.txt', 'w') as note1:
	for data in LIST:
		if data.split('.')[-1] == 'fastq' or data.split('.')[-1] == 'gz':
			if '_R1' in data:
				Name = data.split('/')[-1]
				Name = Name.split('_R1')[0]
				command = f'mkdir {Name}'
				os.system(command)
				Size = os.path.getsize(data)

				name = data.split('_R1')[0]
				First = data
				Second = data.replace('_R1', '_R2')
				note1.write(Name + '\t' + First+ '\t' + Second + '\t' + str(Size) + '\n')
				with open(f'{Name}/SampleSheet.txt', 'w') as note2:
					note2.write(Name + '\t' + First+ '\t' + Second + '\t' + str(Size) + '\n')

			elif '_1.fastq.gz' in data:
				Name = data.split('/')[-1]
				Name = Name.split('_1.fastq.gz')[0]
				command = f'mkdir {Name}'
				os.system(command)
				Size = os.path.getsize(data)

				name = data.split('_1.fastq.gz')[0]
				First = data
				Second = data.replace('_1.fastq.gz', '_2.fastq.gz')
				note1.write(Name + '\t' + First+ '\t' + Second + '\t' + str(Size) + '\n')
				with open(f'{Name}/SampleSheet.txt', 'w') as note2:
					note2.write(Name + '\t' + First+ '\t' + Second + '\t' + str(Size) + '\n')

			elif '_1.fastq' in data:
				Name = data.split('/')[-1]
				Name = Name.split('_1.fastq')[0]
				command = f'mkdir {Name}'
				os.system(command)
				Size = os.path.getsize(data)

				name = data.split('_1.fastq')[0]
				First = data
				Second = data.replace('_1.fastq', '_2.fastq')
				note1.write(Name + '\t' + First+ '\t' + Second + '\t' + str(Size) + '\n')
				with open(f'{Name}/SampleSheet.txt', 'w') as note2:
					note2.write(Name + '\t' + First+ '\t' + Second + '\t' + str(Size) + '\n')
#-----------------------------------------------------------------------------------------#