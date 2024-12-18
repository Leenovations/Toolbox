from lxml import etree
import pandas as pd
#--------------------------------------------------------------------------------------#
tree = etree.parse('/media/src/Classification/ClinVarVCVRelease_00-latest_weekly.xml')
# tree = etree.parse('/media/src/Classification/test.xml')
root = tree.getroot()
#--------------------------------------------------------------------------------------#
Info = root.findall("VariationArchive/ClassifiedRecord")
Total = {}
for info in Info:
    HGVSlist = info.findall("SimpleAllele/HGVSlist/HGVS/NucleotideExpression")
    for hgvslist in HGVSlist:
        if hgvslist.attrib['sequenceAccession'].startswith('NM'):
            NM_accession = hgvslist.attrib
            Total[NM_accession.get('sequenceAccessionVersion')] = {}
            Total[NM_accession.get('sequenceAccessionVersion')]['NMsequenceAccession'] = NM_accession.get('sequenceAccession')
            Total[NM_accession.get('sequenceAccessionVersion')]['NMsequenceVersion'] = NM_accession.get('sequenceVersion')
            Total[NM_accession.get('sequenceAccessionVersion')]['NMchange'] = NM_accession.get('change')
            if 'MANESelect' in NM_accession:
                Total[NM_accession.get('sequenceAccessionVersion')]['MANESelect'] = 'O'
            else:
                Total[NM_accession.get('sequenceAccessionVersion')]['MANESelect'] = 'X'
            # MolecularConsequence = hgvslist.find("../MolecularConsequence").attrib
            # Total[NM_accession.get('sequenceAccessionVersion')]['NMType'] = MolecularConsequence.get('Type')
            if hgvslist.find("../ProteinExpression") != None:
                ProteinExpression = hgvslist.find("../ProteinExpression").attrib
                Total[NM_accession.get('sequenceAccessionVersion')]['NPsequenceAccession'] = ProteinExpression.get('sequenceAccession')
                Total[NM_accession.get('sequenceAccessionVersion')]['NPsequenceVersion'] = ProteinExpression.get('sequenceVersion')
                Total[NM_accession.get('sequenceAccessionVersion')]['NPchange'] = ProteinExpression.get('change')
            else:
                sequenceAccession = None
                sequenceVersion = None
                change = None
                Total[NM_accession.get('sequenceAccessionVersion')]['NPsequenceAccession'] = sequenceAccession
                Total[NM_accession.get('sequenceAccessionVersion')]['NPsequenceVersion'] = sequenceVersion
                Total[NM_accession.get('sequenceAccessionVersion')]['NPchange'] = change
            #--------------------------------------------------------------------------------------#
            Allele_ID = info.find("SimpleAllele")
            Allele_ID = Allele_ID.get("AlleleID")
            Total[NM_accession.get('sequenceAccessionVersion')]['AlleleID'] = Allele_ID
            #--------------------------------------------------------------------------------------#
            Gene = info.find("SimpleAllele/GeneList/Gene")
            gene = Gene.get('Symbol')
            Total[NM_accession.get('sequenceAccessionVersion')]['Symbol'] = gene
            #--------------------------------------------------------------------------------------#
            Fullname = info.find("SimpleAllele/GeneList/Gene")
            FullName = Fullname.get('FullName')
            Total[NM_accession.get('sequenceAccessionVersion')]['FullName'] = FullName
            #--------------------------------------------------------------------------------------#
            Location = info.find("SimpleAllele/GeneList/Gene/Location/CytogeneticLocation")
            Location = Location.text
            Total[NM_accession.get('sequenceAccessionVersion')]['Location'] = Location
            #--------------------------------------------------------------------------------------#
            # Strand = info.find("SimpleAllele/GeneList/Gene/Location/SequenceLocation[@Assembly='GRCh37']")
            # Strand = Strand.get('Strand')
            # Total[NM_accession.get('sequenceAccessionVersion')]['Strand'] = Strand
            #--------------------------------------------------------------------------------------#
            OMIM = info.find("SimpleAllele/GeneList/Gene/OMIM")
            OMIM = OMIM.text
            Total[NM_accession.get('sequenceAccessionVersion')]['OMIM'] = OMIM
            #--------------------------------------------------------------------------------------#
            RCV = info.find("RCVList/RCVAccession")
            RCV_accession = RCV.get('Accession')
            Total[NM_accession.get('sequenceAccessionVersion')]['RCV'] = RCV_accession
            #--------------------------------------------------------------------------------------#
            Class = info.find("Classifications/GermlineClassification/Description").text
            # Synonym =  info.find("Classifications/GermlineClassification/ConditionList/TraitSet/Trait/Symbol/ElementValue").text
            Disease_info =  info.findall("Classifications/GermlineClassification/ConditionList/TraitSet/Trait/Name")

            DISESE_INFO = []
            for (num, di) in enumerate(Disease_info):
                Contents = f'[{num+1}] {di.find("ElementValue").text}'
                DISESE_INFO.append(Contents)
            DISESE_INFO = (', '.join(DISESE_INFO))
            
            Total[NM_accession.get('sequenceAccessionVersion')]['Class'] = Class
            # Total[NM_accession.get('sequenceAccessionVersion')]['Synonym'] = Synonym
            Total[NM_accession.get('sequenceAccessionVersion')]['Disease Info'] = DISESE_INFO
#--------------------------------------------------------------------------------------#
# xml = pd.DataFrame(Total).transpose().reset_index(drop=False)
#--------------------------------------------------------------------------------------#
# xml.to_csv('Clinvariation.annotationinfo.ver.240402.txt', sep='\t', index=False)
#--------------------------------------------------------------------------------------#