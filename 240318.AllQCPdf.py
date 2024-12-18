#!/home/lab/anaconda3/envs/NGS/bin/python3

import os
import pandas as pd
from fpdf import FPDF
from datetime import datetime
from pdf2image import convert_from_path
#----------------------------------------------------------------------------------------#
Sample = pd.read_csv("SampleSheet.txt", sep="\t", header=None)
Name = Sample.iloc[0, 0]
R1 = Sample.iloc[0, 1]
R2 = Sample.iloc[0, 2]
#----------------------------------------------------------------------------------------#
def QCPDF(name):
	Date = datetime.now()

	if os.path.isdir(f'00.PreQC/{name}_1_fastqc'):
		pass
	else:
		command = f'unzip 00.PreQC/{name}_1_fastqc.zip \
					-d 00.PreQC/'
		os.system(command)

	pdf = FPDF()
		
# Adding a page
	pdf.add_page()
		
# set center location of x (210 : A4)
	Center_x = pdf.w / 2 # 105
		
# create a cell
	pdf.set_fill_color(r=100, g=100, b=100)
	pdf.line(Center_x-95, 20, Center_x+95, 20)
	pdf.set_font("Arial", size = 15)
	pdf.text(20, 11, txt = 'WGBS QC')

#Sample Name
	pdf.set_font("Arial", style = 'B', size = 10)
	pdf.text(20, 17, txt = f"Sample : {name}")

#Date
	pdf.set_font("Arial", style = 'B', size = 10)
	pdf.text(170, 17, txt = Date.strftime('%Y-%m-%d'))

#Category 1
	pdf.set_font("Arial", style = 'B', size = 12)
	pdf.text(20, 27, txt = '1. FASTQ Statistics - PreQC (R1)')

#Category1 Image
	pdf.set_font("Arial", size = 9)

	pdf.text(35, 35, txt = "Per base quality")
	pdf.image(f'00.PreQC/{name}_1_fastqc/Images/per_base_quality.png', x = 20, y = 36, w = 50, h = 50, type = 'PNG')

	pdf.text(90, 35, txt = "Per sequence quality")
	pdf.image(f'00.PreQC/{name}_1_fastqc/Images/per_sequence_quality.png', x = 80, y = 36, w = 50, h = 50, type = 'PNG')

	pdf.text(145, 35, txt = "Per base sequence content")
	pdf.image(f'00.PreQC/{name}_1_fastqc/Images/per_base_sequence_content.png', x = 140, y = 36, w = 50, h = 50, type = 'PNG')

	pdf.text(35, 108, txt = "Per sequence gc content")
	pdf.image(f'00.PreQC/{name}_1_fastqc/Images/per_sequence_gc_content.png', x = 20, y = 110, w = 50, h = 50, type = 'PNG')

	pdf.text(90, 108, txt = "per base n content")
	pdf.image(f'00.PreQC/{name}_1_fastqc/Images/per_base_n_content.png', x = 80, y = 110, w = 50, h = 50, type = 'PNG')

	pdf.text(145, 108, txt = "Sequence length distribution")
	pdf.image(f'00.PreQC/{name}_1_fastqc/Images/sequence_length_distribution.png', x = 140, y = 110, w = 50, h = 50, type = 'PNG')

	pdf.text(Center_x - 60, 177, txt = "Duplication levels")
	pdf.image(f'00.PreQC/{name}_1_fastqc/Images/duplication_levels.png', x = Center_x - 75, y = 184, w = 50, h = 50, type = 'PNG')

	pdf.text(Center_x + 40, 177, txt = "Adapter content")
	pdf.image(f'00.PreQC/{name}_1_fastqc/Images/adapter_content.png', x = Center_x + 25, y = 184, w = 50, h = 50, type = 'PNG')

#Category 3 
	pdf.set_fill_color(r=100, g=100, b=100)
	pdf.line(Center_x-95, pdf.h-20, Center_x+95, pdf.h-20)
	pdf.set_font("Arial", style='B', size = 10)
	pdf.set_text_color(204,204,204)
	pdf.text(Center_x, pdf.h-13, txt = '1/4')

#PAGE 2
	if os.path.isdir(f'00.PreQC/{name}_2_fastqc'):
		pass
	else:
		command = f'unzip 00.PreQC/{name}_2_fastqc.zip \
                    -d 00.PreQC/'
		os.system(command)

# Adding a page
	pdf.add_page()
		
# set center location of x (210 : A4)
	Center_x = pdf.w / 2 # 105
		
# create a cell
	pdf.set_fill_color(r=100, g=100, b=100)
	pdf.set_text_color(0, 0, 0)
	pdf.line(Center_x-95, 20, Center_x+95, 20)
	pdf.set_font("Arial", size = 15)
	pdf.text(20, 11, txt = 'WGBS QC')

#Sample Name
	pdf.set_font("Arial", style = 'B', size = 10)
	pdf.text(20, 17, txt = f"Sample : {name}")

#Date
	pdf.set_font("Arial", style = 'B', size = 10)
	pdf.text(170, 17, txt = Date.strftime('%Y-%m-%d'))

#Category 1
	pdf.set_font("Arial", style = 'B', size = 12)
	pdf.text(20, 27, txt = '1. FASTQ Statistics - PreQC (R2)')

#Category1 Image
	pdf.set_font("Arial", size = 9)

	pdf.text(35, 35, txt = "Per base quality")
	pdf.image(f'00.PreQC/{name}_2_fastqc/Images/per_base_quality.png', x = 20, y = 36, w = 50, h = 50, type = 'PNG')

	pdf.text(90, 35, txt = "Per sequence quality")
	pdf.image(f'00.PreQC/{name}_2_fastqc/Images/per_sequence_quality.png', x = 80, y = 36, w = 50, h = 50, type = 'PNG')

	pdf.text(145, 35, txt = "Per base sequence content")
	pdf.image(f'00.PreQC/{name}_2_fastqc/Images/per_base_sequence_content.png', x = 140, y = 36, w = 50, h = 50, type = 'PNG')

	pdf.text(35, 108, txt = "Per sequence gc content")
	pdf.image(f'00.PreQC/{name}_2_fastqc/Images/per_sequence_gc_content.png', x = 20, y = 110, w = 50, h = 50, type = 'PNG')

	pdf.text(90, 108, txt = "per base n content")
	pdf.image(f'00.PreQC/{name}_2_fastqc/Images/per_base_n_content.png', x = 80, y = 110, w = 50, h = 50, type = 'PNG')

	pdf.text(145, 108, txt = "Sequence length distribution")
	pdf.image(f'00.PreQC/{name}_2_fastqc/Images/sequence_length_distribution.png', x = 140, y = 110, w = 50, h = 50, type = 'PNG')

	pdf.text(Center_x - 60, 177, txt = "Duplication levels")
	pdf.image(f'00.PreQC/{name}_2_fastqc/Images/duplication_levels.png', x = Center_x - 75, y = 184, w = 50, h = 50, type = 'PNG')

	pdf.text(Center_x + 40, 177, txt = "Adapter content")
	pdf.image(f'00.PreQC/{name}_2_fastqc/Images/adapter_content.png', x = Center_x + 25, y = 184, w = 50, h = 50, type = 'PNG')

#Category 3 
	pdf.set_fill_color(r=100, g=100, b=100)
	pdf.line(Center_x-95, pdf.h-20, Center_x+95, pdf.h-20)
	pdf.set_font("Arial", style='B', size = 10)
	pdf.set_text_color(204,204,204)
	pdf.text(Center_x, pdf.h-13, txt = '2/4')

	if os.path.isdir(f'01.PostQC/{name}_val_1_fastqc'):
		pass
	else:
		command = f'unzip 01.PostQC/{name}_val_1_fastqc.zip \
                    -d 01.PostQC/'
		os.system(command)

# Adding a page
	pdf.add_page()
		
# set center location of x (210 : A4)
	Center_x = pdf.w / 2 # 105
		
# create a cell
	pdf.set_fill_color(r=100, g=100, b=100)
	pdf.set_text_color(0,0,0)
	pdf.line(Center_x-95, 20, Center_x+95, 20)
	pdf.set_font("Arial", size = 15)
	pdf.text(20, 11, txt = 'WGBS QC')

#Sample Name
	pdf.set_font("Arial", style = 'B', size = 10)
	pdf.text(20, 17, txt = f"Sample : {name}")

#Date
	pdf.set_font("Arial", style = 'B', size = 10)
	pdf.text(170, 17, txt = Date.strftime('%Y-%m-%d'))

#Category 1
	pdf.set_font("Arial", style = 'B', size = 12)
	pdf.text(20, 27, txt = '2. FASTQ Statistics - PostQC (R1)')

#Category1 Image
	pdf.set_font("Arial", size = 9)

	pdf.text(35, 35, txt = "Per base quality")
	pdf.image(f'01.PostQC/{name}_val_1_fastqc/Images/per_base_quality.png', x = 20, y = 36, w = 50, h = 50, type = 'PNG')

	pdf.text(90, 35, txt = "Per sequence quality")
	pdf.image(f'01.PostQC/{name}_val_1_fastqc/Images/per_sequence_quality.png', x = 80, y = 36, w = 50, h = 50, type = 'PNG')

	pdf.text(145, 35, txt = "Per base sequence content")
	pdf.image(f'01.PostQC/{name}_val_1_fastqc/Images/per_base_sequence_content.png', x = 140, y = 36, w = 50, h = 50, type = 'PNG')

	pdf.text(35, 108, txt = "Per sequence gc content")
	pdf.image(f'01.PostQC/{name}_val_1_fastqc/Images/per_sequence_gc_content.png', x = 20, y = 110, w = 50, h = 50, type = 'PNG')

	pdf.text(90, 108, txt = "per base n content")
	pdf.image(f'01.PostQC/{name}_val_1_fastqc/Images/per_base_n_content.png', x = 80, y = 110, w = 50, h = 50, type = 'PNG')

	pdf.text(145, 108, txt = "Sequence length distribution")
	pdf.image(f'01.PostQC/{name}_val_1_fastqc/Images/sequence_length_distribution.png', x = 140, y = 110, w = 50, h = 50, type = 'PNG')

	pdf.text(Center_x - 60, 177, txt = "Duplication levels")
	pdf.image(f'01.PostQC/{name}_val_1_fastqc/Images/duplication_levels.png', x = Center_x - 75, y = 184, w = 50, h = 50, type = 'PNG')

	pdf.text(Center_x + 40, 177, txt = "Adapter content")
	pdf.image(f'01.PostQC/{name}_val_1_fastqc/Images/adapter_content.png', x = Center_x + 25, y = 184, w = 50, h = 50, type = 'PNG')

#Category 3 
	pdf.set_fill_color(r=100, g=100, b=100)
	pdf.line(Center_x-95, pdf.h-20, Center_x+95, pdf.h-20)
	pdf.set_font("Arial", style='B', size = 10)
	pdf.set_text_color(204,204,204)
	pdf.text(Center_x, pdf.h-13, txt = '3/4')

	if os.path.isdir(f'01.PostQC/{name}_val_2_fastqc'):
		pass
	else:
		command = f'unzip 01.PostQC/{name}_val_2_fastqc.zip \
                    -d 01.PostQC/'
		os.system(command)

# Adding a page
	pdf.add_page()
		
# set center location of x (210 : A4)
	Center_x = pdf.w / 2 # 105
		
# create a cell
	pdf.set_fill_color(r=100, g=100, b=100)
	pdf.set_text_color(0,0,0)
	pdf.line(Center_x-95, 20, Center_x+95, 20)
	pdf.set_font("Arial", size = 15)
	pdf.text(20, 11, txt = 'WGBS QC')

#Sample Name
	pdf.set_font("Arial", style = 'B', size = 10)
	pdf.text(20, 17, txt = f"Sample : {name}")

#Date
	pdf.set_font("Arial", style = 'B', size = 10)
	pdf.text(170, 17, txt = Date.strftime('%Y-%m-%d'))

#Category 1
	pdf.set_font("Arial", style = 'B', size = 12)
	pdf.text(20, 27, txt = '2. FASTQ Statistics - PostQC (R2)')

#Category1 Image
	pdf.set_font("Arial", size = 9)

	pdf.text(35, 35, txt = "Per base quality")
	pdf.image(f'01.PostQC/{name}_val_2_fastqc/Images/per_base_quality.png', x = 20, y = 36, w = 50, h = 50, type = 'PNG')

	pdf.text(90, 35, txt = "Per sequence quality")
	pdf.image(f'01.PostQC/{name}_val_2_fastqc/Images/per_sequence_quality.png', x = 80, y = 36, w = 50, h = 50, type = 'PNG')

	pdf.text(145, 35, txt = "Per base sequence content")
	pdf.image(f'01.PostQC/{name}_val_2_fastqc/Images/per_base_sequence_content.png', x = 140, y = 36, w = 50, h = 50, type = 'PNG')

	pdf.text(35, 108, txt = "Per sequence gc content")
	pdf.image(f'01.PostQC/{name}_val_2_fastqc/Images/per_sequence_gc_content.png', x = 20, y = 110, w = 50, h = 50, type = 'PNG')

	pdf.text(90, 108, txt = "per base n content")
	pdf.image(f'01.PostQC/{name}_val_2_fastqc/Images/per_base_n_content.png', x = 80, y = 110, w = 50, h = 50, type = 'PNG')

	pdf.text(145, 108, txt = "Sequence length distribution")
	pdf.image(f'01.PostQC/{name}_val_2_fastqc/Images/sequence_length_distribution.png', x = 140, y = 110, w = 50, h = 50, type = 'PNG')

	pdf.text(Center_x - 60, 177, txt = "Duplication levels")
	pdf.image(f'01.PostQC/{name}_val_2_fastqc/Images/duplication_levels.png', x = Center_x - 75, y = 184, w = 50, h = 50, type = 'PNG')

	pdf.text(Center_x + 40, 177, txt = "Adapter content")
	pdf.image(f'01.PostQC/{name}_val_2_fastqc/Images/adapter_content.png', x = Center_x + 25, y = 184, w = 50, h = 50, type = 'PNG')

#Category 3 
	pdf.set_fill_color(r=100, g=100, b=100)
	pdf.line(Center_x-95, pdf.h-20, Center_x+95, pdf.h-20)

	pdf.set_font("Arial", style='B', size = 10)
	pdf.set_text_color(204,204,204)
	pdf.text(Center_x, pdf.h-13, txt = '4/4')
# save the pdf
	pdf.output(f"/labmed/01.ALL/01.WGBS/Results/00.QCReports/{name}.QC.pdf")
#----------------------------------------------------------------------------------------#
#def pdfconverter(name):
#    images = convert_from_path(f"/labmed/01.ALL/01.WGBS/Results/00.QCReports/{name}.QC.pdf")
#
#    for page, image in enumerate(images):
#        image.save(f"/labmed/01.ALL/01.WGBS/Results/00.QCReports/{name}.QC.page{page}.jpg", "JPEG")
#----------------------------------------------------------------------------------------#
QCPDF(Name)
#pdfconverter(Name)
