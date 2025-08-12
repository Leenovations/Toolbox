#!/usr/bin/python3
import sys
import os
#-----------------------------------------------------------------------------------------#
Class = sys.argv[1]
File_Type = sys.argv[2]
LIST = sys.argv[3:]
#-----------------------------------------------------------------------------------------#
if File_Type == 'FASTQ':
	if len(LIST) % 2 == 0:
		pass
	elif 'bam' in LIST[0] or 'vcf' in LIST[0]:
		raise ValueError("\033[91mCheck your file type!!!\033[0m")
	else:
		raise ValueError("\033[91mThe number of raw data files is odd\033[0m")
elif File_Type == 'BAM':
	os.makedirs('00.FASTQ', exist_ok=True)
	if 'fastq' in LIST[0] or 'vcf' in LIST[0]:
		raise ValueError("\033[91mCheck your file type!!!\033[0m")
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

				First = data
				Second = data.replace('_R1', '_R2')
				note1.write(Name + '\t' + First + '\t' + Second + '\t' + str(Size) + '\n')
				with open(f'{Name}/SampleSheet.txt', 'w') as note2:
					note2.write(Name + '\t' + First + '\t' + Second + '\t' + str(Size) + '\n')

			elif '_1.fastq.gz' in data:
				Name = data.split('/')[-1]
				Name = Name.split('_1.fastq.gz')[0]
				command = f'mkdir {Name}'
				os.system(command)
				Size = os.path.getsize(data)

				First = data
				Second = data.replace('_1.fastq.gz', '_2.fastq.gz')
				note1.write(Name + '\t' + First + '\t' + Second + '\t' + str(Size) + '\n')
				with open(f'{Name}/SampleSheet.txt', 'w') as note2:
					note2.write(Name + '\t' + First + '\t' + Second + '\t' + str(Size) + '\n')

			elif '_1.fastq' in data:
				Name = data.split('/')[-1]
				Name = Name.split('_1.fastq')[0]
				command = f'mkdir {Name}'
				os.system(command)
				Size = os.path.getsize(data)

				First = data
				Second = data.replace('_1.fastq', '_2.fastq')
				note1.write(Name + '\t' + First + '\t' + Second + '\t' + str(Size) + '\n')
				with open(f'{Name}/SampleSheet.txt', 'w') as note2:
					note2.write(Name + '\t' + First + '\t' + Second + '\t' + str(Size) + '\n')

		elif data.split('.')[-1] == 'bam':
			Name = data.split('/')[-1]
			Name = Name.split('.bam')[0]
			command = f"touch 00.FASTQ/{Name}_R1.fastq.gz 00.FASTQ/{Name}_R2.fastq.gz"
			os.system(command)
			command = f'mkdir {Name}'
			os.system(command)
			Size = os.path.getsize(data)

			note1.write(Name + '\t' + data + '\t' + data + '\t' + str(Size) + '\n')
			with open(f'{Name}/SampleSheet.txt', 'w') as note2:
				note2.write(Name + '\t' + data + '\t' + data + '\t' + str(Size) + '\n')
#-----------------------------------------------------------------------------------------#