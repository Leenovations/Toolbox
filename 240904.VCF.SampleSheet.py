#!/usr/bin/python3
import sys
import os

Class = sys.argv[1]
LIST = sys.argv[2:]

with open('VCFDatalist.txt', 'w') as note2:
	for data in LIST:
		Dir_name = data.split('.vcf')[0]
		command = f'mkdir {Dir_name}'
		os.system(command)
		note2.write(data + '\n')
		
with open('VCFSampleSheet.txt', 'w') as note1:
	for data in LIST:
		Name = data.split('/')[-1]
		Path = os.getcwd()
		Dir_name = data.split('/')[-1].split('.vcf')[0]
		Whole_path = Path + '/' + Dir_name
		Size = os.path.getsize(data)
		note1.write(Dir_name + '\t' + Whole_path + '.vcf' + '\t' + Whole_path + '.vcf' + '\t' + str(Size) + '\n')
		
		with open(f'{Whole_path}/VCFSampleSheet.txt', 'w') as note2:
			Name = data.split('/')[-1]
			Path = data
			note2.write(Dir_name + '\t' + Whole_path + '.vcf' + '\t' + Whole_path + '.vcf' + '\t' + str(Size) + '\n')