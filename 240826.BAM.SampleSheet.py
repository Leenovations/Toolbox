#!/usr/bin/python3
import sys
import os

Class = sys.argv[1]
LIST = sys.argv[2:]

with open('BAMDatalist.txt', 'w') as note2:
	for data in LIST:
		BAM = data.split('/')[-1]
		Name = BAM.split('.')[0]

		command = f'mkdir {Name}'
		os.system(command)

		if os.path.isdir(f"{Name}/03.Output"):
			pass
		else:
			command = f"mkdir -p {Name}/03.Output"
			os.system(command)

		note2.write(data + '\n')
		
with open('BAMSampleSheet.txt', 'w') as note1:
	for data in LIST:
		BAM = data.split('/')[-1]
		Name = BAM.split('.')[0]
		
		Data = data
		Size = os.path.getsize(data)

		note1.write(Name + '\t' + Data + '\t' + Data + '\t' + str(Size) + '\n')
		
		with open(f'{Name}/BAMSampleSheet.txt', 'w') as note2:
			Data = data
			note2.write(Name + '\t' + Data + '\t' + Data + '\t' + str(Size) + '\n')