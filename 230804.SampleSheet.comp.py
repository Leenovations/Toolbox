#!/usr/bin/python3
import sys
import os
import glob

LIST = sys.argv[1:]

with open('SampleSheet.txt', 'w') as note1:
	for fastq in LIST:
		if '_R1' in fastq:
			Name = fastq.split('/')[-1]
			Name = Name.split('_R1')[0]
			command = f'mkdir {Name}'
			os.system(command)

			name = fastq.split('_R1')[0]
			First = fastq
			Second = fastq.replace('_R1', '_R2')
			note1.write(Name + '\t' + First+ '\t' + Second + '\n')

			with open(f'{Name}/SampleSheet.txt', 'w') as note2:
				name = fastq.split('_R1')[0]
				First = fastq
				Second = fastq.replace('_R1', '_R2')
				note2.write(Name + '\t' + First+ '\t' + Second + '\n')

			# with open(f'{Name}/PWD.conf', 'w') as note:
			# 	note.write(os.getcwd() + '/' + {Name} + '\n')
		
		elif '_1.fastq.gz' in fastq:
			Name = fastq.split('/')[-1]
			Name = Name.split('_1.fastq.gz')[0]
			command = f'mkdir {Name}'
			os.system(command)

			name = fastq.split('_1.fastq.gz')[0]
			First = fastq
			Second = fastq.replace('_1.fastq.gz', '_2.fastq.gz')
			note1.write(Name + '\t' + First+ '\t' + Second + '\n')

			with open(f'{Name}/SampleSheet.txt', 'w') as note2:
				name = fastq.split('_1.fastq.gz')[0]
				First = fastq
				Second = fastq.replace('_1.fastq.gz', '_2.fastq.gz')
				note2.write(Name + '\t' + First+ '\t' + Second + '\n')

			# with open(f'{Name}/PWD.conf', 'w') as note:
			# 	note.write(os.getcwd + '/' + {Name} + '\n')