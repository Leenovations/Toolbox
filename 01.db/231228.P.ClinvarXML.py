import xml.etree.ElementTree as ET
import pandas as pd
import argparse
import sys
#----------------------------------------------------------#
parser = argparse.ArgumentParser(description='Code Usage')
parser.add_argument('1', metavar='<xml>', help='Set xml file')
parser.add_argument('2', metavar='<Output>', help='Set output Name')
args = parser.parse_args()
#----------------------------------------------------------#
# XML 파일 로드
tree = ET.parse('test.xml')
root = tree.getroot()

# 각 Product에 대한 정보 추출
for product in root.findall('.//Product'):
    name = product.find('Name').text
    price = float(product.find('Price').text)
    
    print(f"Product: {name}, Price: {price}")
#----------------------------------------------------------#