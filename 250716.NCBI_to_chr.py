nc_to_chr = {
    ">NC_000001": "chr1",
    ">NC_000002": "chr2",
    ">NC_000003": "chr3",
    ">NC_000004": "chr4",
    ">NC_000005": "chr5",
    ">NC_000006": "chr6",
    ">NC_000007": "chr7",
    ">NC_000008": "chr8",
    ">NC_000009": "chr9",
    ">NC_000010": "chr10",
    ">NC_000011": "chr11",
    ">NC_000012": "chr12",
    ">NC_000013": "chr13",
    ">NC_000014": "chr14",
    ">NC_000015": "chr15",
    ">NC_000016": "chr16",
    ">NC_000017": "chr17",
    ">NC_000018": "chr18",
    ">NC_000019": "chr19",
    ">NC_000020": "chr20",
    ">NC_000021": "chr21",
    ">NC_000022": "chr22",
    ">NC_000023": "chrX",
    ">NC_000024": "chrY",
    ">NC_012920": "chrM"}

DICT_SEQ = {}
with open('/media/src/DB/hg38/GCF_000001405.40_GRCh38.p14_genomic.fa', 'r') as fa:
    for line in fa:
        line = line.strip()
        if line.startswith('>'):
            Chr = line.split(' ')[0]
        DICT_SEQ[Chr] = []
        DICT_SEQ[Chr].append(line)