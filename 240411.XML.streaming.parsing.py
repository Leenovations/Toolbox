import xml.etree.ElementTree as ET
from lxml import etree
import pandas as pd
#-------------------------------------------------------------------------------------------------------------------#
# def process_sections(xml_file):
#     header = ['NM', 'NMsequenceAccession', 'NMsequenceVersion', 'NMchange', 'Type', 'Symbol' ,'MANESelect', 'NPsequenceAccession', 'NPsequenceVersion', 'NPchange', 'AlleleID', 'RCV', 'Class', 'Synonym', 'Disease Info', 'Strand']
#     context = ET.iterparse(xml_file, events=('start', 'end'))
#     _, root = next(context)
    
#     with open('/media/src/hg19/06.Annotation/Clinvar.annotation.txt', 'w') as note1:
#         note1.write('\t'.join(header) + '\n')
#         for event, elem in context:
#             Total = {}
#             if event == 'start' and elem.tag == 'ClassifiedRecord':
#                 HGVSList = elem.findall('./SimpleAllele/HGVSlist/HGVS')
#                 for hgvslist in HGVSList:
#                     if hgvslist.attrib['Type'] == 'coding':
#                         if hgvslist.find('NucleotideExpression') is not None: 
#                             if hgvslist.find('NucleotideExpression').attrib['sequenceAccession'].startswith('NM'):
#                                 Type = hgvslist.find('MolecularConsequence')
#                                 if Type is not None:
#                                     Type = hgvslist.find('MolecularConsequence').attrib['Type']
#                                     NM_accession = hgvslist.find('NucleotideExpression').attrib
#                                     Total[NM_accession.get('sequenceAccessionVersion')] = {}
#                                     Total[NM_accession.get('sequenceAccessionVersion')]['NM'] = NM_accession.get('sequenceAccession') + '.' + NM_accession.get('sequenceVersion')
#                                     if 'MANESelect' in NM_accession:
#                                         Total[NM_accession.get('sequenceAccessionVersion')]['MANESelect'] = 'O'
#                                     else:
#                                         Total[NM_accession.get('sequenceAccessionVersion')]['MANESelect'] = 'X'
#                                     Total[NM_accession.get('sequenceAccessionVersion')]['NMchange'] = NM_accession.get('change')
#                                     Total[NM_accession.get('sequenceAccessionVersion')]['Type'] = Type

#                                     Symbol = elem.find("SimpleAllele/GeneList/Gene")
#                                     if Symbol is not None:
#                                         Symbol = Symbol.get('Symbol')
#                                     else:
#                                         Symbol = '.'
#                                     Total[NM_accession.get('sequenceAccessionVersion')]['Symbol'] = Symbol

#                                     if hgvslist.find("ProteinExpression") != None:
#                                         ProteinExpression = hgvslist.find("ProteinExpression").attrib
#                                         Total[NM_accession.get('sequenceAccessionVersion')]['NPsequenceAccession'] = ProteinExpression.get('sequenceAccession')
#                                         Total[NM_accession.get('sequenceAccessionVersion')]['NPsequenceVersion'] = ProteinExpression.get('sequenceVersion')
#                                         Total[NM_accession.get('sequenceAccessionVersion')]['NPchange'] = ProteinExpression.get('change')
#                                     else:
#                                         sequenceAccession = '.'
#                                         sequenceVersion = '.'
#                                         change = '.'
#                                         Total[NM_accession.get('sequenceAccessionVersion')]['NPsequenceAccession'] = sequenceAccession
#                                         Total[NM_accession.get('sequenceAccessionVersion')]['NPsequenceVersion'] = sequenceVersion
#                                         Total[NM_accession.get('sequenceAccessionVersion')]['NPchange'] = change

#                                     Allele_ID = elem.find("SimpleAllele")
#                                     Allele_ID = Allele_ID.get("AlleleID")
#                                     Total[NM_accession.get('sequenceAccessionVersion')]['AlleleID'] = Allele_ID

#                                     RCV = elem.find("RCVList/RCVAccession")
#                                     if RCV is not None:
#                                         RCV_accession = RCV.attrib['Accession']
#                                     else:
#                                         RCV_accession = '.'
#                                     Total[NM_accession.get('sequenceAccessionVersion')]['RCV'] = RCV_accession

#                                     Fullname = elem.find("SimpleAllele/GeneList/Gene")
#                                     if Fullname is not None:
#                                         FullName = Fullname.get('FullName')
#                                     else:
#                                         FullName = '.'
#                                     Total[NM_accession.get('sequenceAccessionVersion')]['FullName'] = FullName
#                                     #--------------------------------------------------------------------------------------#
#                                     Location = elem.find("SimpleAllele/GeneList/Gene/Location/CytogeneticLocation")
#                                     if Location is not None:
#                                         Location = Location.text
#                                     else:
#                                         Location = '.'
#                                     Total[NM_accession.get('sequenceAccessionVersion')]['Location'] = Location
#                                     #--------------------------------------------------------------------------------------#
#                                     OMIM = elem.find("SimpleAllele/GeneList/Gene/OMIM")
#                                     if OMIM is not None:
#                                         OMIM = OMIM.text
#                                     else:
#                                         OMIM = '.' 
#                                     Total[NM_accession.get('sequenceAccessionVersion')]['OMIM'] = OMIM
#                                     #--------------------------------------------------------------------------------------#
#                                     Strand = elem.find("SimpleAllele/GeneList/Gene/Location/SequenceLocation[@Assembly='GRCh37']")
#                                     if Strand is not None:
#                                         Strand = Strand.get('Strand')
#                                     else:
#                                         Strand = '.' 
#                                     Total[NM_accession.get('sequenceAccessionVersion')]['Strand'] = Strand
#                                     #--------------------------------------------------------------------------------------# 
#                                     Class = elem.find("Classifications/GermlineClassification/Description")
#                                     if Class is not None:
#                                         Class = Class.text
#                                     else:
#                                         Class = '.' 

#                                     Synonym =  elem.find("Classifications/GermlineClassification/ConditionList/TraitSet/Trait/Symbol/ElementValue")
#                                     if Synonym is not None:
#                                         Synonym = Synonym.text
#                                     else:
#                                         Synonym = '.' 

#                                     Disease_elem =  elem.findall("Classifications/GermlineClassification/ConditionList/TraitSet/Trait/Name")
#                                     DISESE_INFO = []
#                                     for (num, di) in enumerate(Disease_elem):
#                                         Contents = di.find("ElementValue")
#                                         if Contents is not None:
#                                             Contents = f'[{num+1}] {di.find("ElementValue").text}'
#                                             DISESE_INFO.append(Contents)
#                                         else:
#                                             Contents = '.' 
#                                             DISESE_INFO.append(Contents)
#                                     DISESE_INFO = (', '.join(DISESE_INFO))

#                                     Total[NM_accession.get('sequenceAccessionVersion')]['Class'] = Class
#                                     Total[NM_accession.get('sequenceAccessionVersion')]['Synonym'] = Synonym
#                                     Total[NM_accession.get('sequenceAccessionVersion')]['Disease Info'] = DISESE_INFO

#                                 else :
#                                     Type = '.'
#                                     NM_accession = hgvslist.find('NucleotideExpression').attrib
#                                     Total[NM_accession.get('sequenceAccessionVersion')] = {}
#                                     Total[NM_accession.get('sequenceAccessionVersion')]['NM'] = NM_accession.get('sequenceAccession') + '.' + NM_accession.get('sequenceVersion')
#                                     if 'MANESelect' in NM_accession:
#                                         Total[NM_accession.get('sequenceAccessionVersion')]['MANESelect'] = 'O'
#                                     else:
#                                         Total[NM_accession.get('sequenceAccessionVersion')]['MANESelect'] = 'X'                                    
#                                     Total[NM_accession.get('sequenceAccessionVersion')]['NMchange'] = NM_accession.get('change')
#                                     Total[NM_accession.get('sequenceAccessionVersion')]['Type'] = Type

#                                     Symbol = elem.find("SimpleAllele/GeneList/Gene")
#                                     if Symbol is not None:
#                                         Symbol = Symbol.get('Symbol')
#                                     else:
#                                         Symbol = '.'
#                                     Total[NM_accession.get('sequenceAccessionVersion')]['Symbol'] = Symbol

#                                     if hgvslist.find("ProteinExpression") != None:
#                                         ProteinExpression = hgvslist.find("ProteinExpression").attrib
#                                         Total[NM_accession.get('sequenceAccessionVersion')]['NPsequenceAccession'] = ProteinExpression.get('sequenceAccession')
#                                         Total[NM_accession.get('sequenceAccessionVersion')]['NPsequenceVersion'] = ProteinExpression.get('sequenceVersion')
#                                         Total[NM_accession.get('sequenceAccessionVersion')]['NPchange'] = ProteinExpression.get('change')
#                                     else:
#                                         sequenceAccession = '.'
#                                         sequenceVersion = '.'
#                                         change = '.'
#                                         Total[NM_accession.get('sequenceAccessionVersion')]['NPsequenceAccession'] = sequenceAccession
#                                         Total[NM_accession.get('sequenceAccessionVersion')]['NPsequenceVersion'] = sequenceVersion
#                                         Total[NM_accession.get('sequenceAccessionVersion')]['NPchange'] = change

#                                     Allele_ID = elem.find("SimpleAllele")
#                                     Allele_ID = Allele_ID.get("AlleleID")
#                                     Total[NM_accession.get('sequenceAccessionVersion')]['AlleleID'] = Allele_ID

#                                     RCV = elem.find("RCVList/RCVAccession")
#                                     if RCV is not None:
#                                         RCV_accession = RCV.attrib['Accession']
#                                     else:
#                                         RCV_accession = '.'
#                                     Total[NM_accession.get('sequenceAccessionVersion')]['RCV'] = RCV_accession

#                                     Fullname = elem.find("SimpleAllele/GeneList/Gene")
#                                     if Fullname is not None:
#                                         FullName = Fullname.get('FullName')
#                                     else:
#                                         FullName = '.'
#                                     Total[NM_accession.get('sequenceAccessionVersion')]['FullName'] = FullName
#                                     #--------------------------------------------------------------------------------------#
#                                     Location = elem.find("SimpleAllele/GeneList/Gene/Location/CytogeneticLocation")
#                                     if Location is not None:
#                                         Location = Location.text
#                                     else:
#                                         Location = '.'
#                                     Total[NM_accession.get('sequenceAccessionVersion')]['Location'] = Location
#                                     #--------------------------------------------------------------------------------------#
#                                     OMIM = elem.find("SimpleAllele/GeneList/Gene/OMIM")
#                                     if OMIM is not None:
#                                         OMIM = OMIM.text
#                                     else:
#                                         OMIM = '.' 
#                                     Total[NM_accession.get('sequenceAccessionVersion')]['OMIM'] = OMIM
#                                     #--------------------------------------------------------------------------------------#
#                                     Strand = elem.find("SimpleAllele/GeneList/Gene/Location/SequenceLocation[@Assembly='GRCh37']")
#                                     if Strand is not None:
#                                         Strand = Strand.get('Strand')
#                                     else:
#                                         Strand = '.' 
#                                     Total[NM_accession.get('sequenceAccessionVersion')]['Strand'] = Strand
#                                     #--------------------------------------------------------------------------------------# 
#                                     Class = elem.find("Classifications/GermlineClassification/Description")
#                                     if Class is not None:
#                                         Class = Class.text
#                                     else:
#                                         Class = '.' 
#                                     Synonym =  elem.find("Classifications/GermlineClassification/ConditionList/TraitSet/Trait/Symbol/ElementValue")
#                                     if Synonym is not None:
#                                         Synonym = Synonym.text
#                                     else:
#                                         Synonym = '.'

#                                     Disease_elem =  elem.findall("Classifications/GermlineClassification/ConditionList/TraitSet/Trait/Name")
#                                     DISESE_INFO = []
#                                     for (num, di) in enumerate(Disease_elem):
#                                         Contents = di.find("ElementValue")
#                                         if Contents is not None:
#                                             Contents = f'[{num+1}] {di.find("ElementValue")}'
#                                             DISESE_INFO.append(Contents)
#                                         else:
#                                             Contents = '.' 
#                                             DISESE_INFO.append(Contents)
#                                     DISESE_INFO = (', '.join(DISESE_INFO))

#                                     Total[NM_accession.get('sequenceAccessionVersion')]['Class'] = Class
#                                     Total[NM_accession.get('sequenceAccessionVersion')]['Synonym'] = Synonym
#                                     Total[NM_accession.get('sequenceAccessionVersion')]['Disease Info'] = DISESE_INFO

#                 for key in Total.keys():
#                     for vkey in Total[key].keys():
#                         if Total[key][vkey] is None:
#                             Total[key][vkey] = '.'

#                 # print(len(Total.values()))
#                 if len(Total.values()) >= 1 :
#                     for key in Total.keys():
#                         Value = Total[key].values()
#                         Value = '\t'.join(Value) + '\n'
#                         note1.write(Value)
# #---------------------------------------------------------------------------------------------------------------------------#
# def lmxl_parsing(xml_file):
#     tree = etree.parse(xml_file)
#     root = tree.getroot()

#     for variation in root.xpath("VariationArchive"):
#         variation_id = variation.attrib.get('VariationID')  # Variation ID 추출
#         variation_name = variation.attrib.get('VariationName')  # Variation Name 추출
#         gene_symbol = variation.xpath(".//Gene/@Symbol")[0] if variation.xpath(".//Gene/@Symbol") else "N/A"
#         VariationID = variation.attrib.get('Accession') + '.' + variation.attrib.get('Version')
#     #-----------------------------------------------------------------------------------------------------------------------#    
#     Species = root.findtext('.//Species')
#     #-----------------------------------------------------------------------------------------------------------------------#
#     GeneSymbol = root.find('.//Gene').get('Symbol')
#     FULLNAME = root.find('.//Gene').get('FullName')
#     HGNCID = root.find('.//Gene').get('HGNC_ID').split(':')[1]
#     Cytoband = root.findtext('.//CytogeneticLocation')
#     #-----------------------------------------------------------------------------------------------------------------------#
#     SequenceLocation = root.findall('.//Location//SequenceLocation')
#     for location in SequenceLocation:
#         Assembly = location.get('Assembly')    
#         Accession = location.get('Accession')
#         Chr = location.get('Chr')
#         VCF_post = location.get('positionVCF')
#         Ref = location.get('referenceAlleleVCF')
#         Alt = location.get('alternateAlleleVCF')
#         strand = location.get('Strand')
#     #-----------------------------------------------------------------------------------------------------------------------#
#     Omim = root.findtext('.//GeneList//OMIM')
#     #-----------------------------------------------------------------------------------------------------------------------#
#     HGVS_list = root.findall('.//HGVS')
#     for hgvs in HGVS_list:
#         Assembly = hgvs.get('Assembly')
#         Type = hgvs.get('Type')
        
#         if Assembly == "GRCh37":
#             Sub = hgvs.findall('.//NucleotideExpression')
#             for sub in Sub:
#                 sequenceAccessionVersion = sub.get('sequenceAccessionVersion')
#                 sequenceAccession = sub.get('sequenceAccession')
#                 change = sub.get('change')

#         elif Assembly == "GRCh38":
#             Sub = hgvs.findall('.//NucleotideExpression')
#             for sub in Sub:
#                 sequenceAccessionVersion = sub.get('sequenceAccessionVersion')
#                 sequenceAccession = sub.get('sequenceAccession')
#                 change = sub.get('change')
#         else:
#             Sub = hgvs.findall('.//NucleotideExpression')
#             for sub in Sub:
#                 sequenceAccessionVersion = sub.get('sequenceAccessionVersion')
#                 sequenceAccession = sub.get('sequenceAccession')
#                 change = sub.get('change')
#     #-----------------------------------------------------------------------------------------------------------------------#
#     XRefList = root.findall('.//XRefList')
#     for xref in XRefList:
#         for Sub in xref:
#             Type = Sub.get('Type')
#             DB = Sub.get('DB')
#             ID = Sub.get('ID')

#             if Type:
#                 pass
#     #-----------------------------------------------------------------------------------------------------------------------#
#     RCV = root.find('.//RCVAccession')
#     title = RCV.get('Title')
#     accession = RCV.get('Accession') + '.' + RCV.get('Version')
#     ClassifiedCondition = RCV.find('.//ClassifiedCondition')
#     ClassifiedConditionDB = ClassifiedCondition.get('DB')
#     ClassifiedConditionID = ClassifiedCondition.get('ID')
#     condition = RCV.findtext('.//ClassifiedCondition')
#     classification = RCV.findtext('.//Description')
#     #-----------------------------------------------------------------------------------------------------------------------#
#     Origin = root.findall('.//VariationArchive')
#     for origin in Origin:
#         A = origin.findall('.//Origin')
#         for i in A:
#             print(i.findtext('.//Origin'))
#     #-----------------------------------------------------------------------------------------------------------------------#
# #---------------------------------------------------------------------------------------------------------------------------#
# def xml_2_csv(xml, output):
#     df = pd.read_xml(xml)
#     df.to_csv(output, index=False, sep='\t')
#---------------------------------------------------------------------------------------------------------------------------#
def test(xml):
    import os
    import pandas as pd
    import xml.etree.ElementTree as ET

    tree = ET.parse(xml)
    root = tree.getroot()
    
    data = []
    for elem in root:
        data.append(elem.attrib)
    df = pd.DataFrame(data)
    
    # DataFrame을 엑셀 파일로 저장
    df.to_csv('ClinvarXML.tsv', index=False, sep='\t')
#---------------------------------------------------------------------------------------------------------------------------#
if __name__ == "__main__":
    xml_file_1 = "/media/src/Classification/ClinVarVCVRelease_00-latest_weekly.xml"
    xml_file_2 = "/media/src/Classification/test.xml"
    test(xml_file_1)