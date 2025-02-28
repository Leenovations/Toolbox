library(TCC)
library(readxl)
library(openxlsx)
library(dplyr)
#------------------------------------------------------------------------------#
Gene <- read.table('/media/src/hg19/00.RNA/hg19.GENCODE.v44.GeneLength.txt', 
                   sep='\t', 
                   col.names = c('ID', 'Type', 'GeneSymbol', 'Length'))
Gene <- list(ID=Gene$ID, GeneSymbol=Gene$GeneSymbol)
#------------------------------------------------------------------------------#
raw_count <- read_excel("/labmed/01.AML/240123.AML.Total.Info.xlsx", sheet='RNA_ReadCount_New')
raw_count <- data.frame(raw_count)
rownames(raw_count) <- raw_count$ID
raw_count <- as.data.frame(raw_count[,-1:-2])
raw_count <- raw_count %>% select(-c('CR1', 'CR3', 'CR10', 'CR13'))
group <- rep(c('CR','NR'), c(4,5))
#------------------------------------------------------------------------------#  
tcc <- new("TCC", raw_count, group)
tcc <- filterLowCountGenes(tcc)
#------------------------------------------------------------------------------#
type <- "deseq2"
if (type == "edger"){
  tcc <- calcNormFactors(tcc, norm.method="tmm", test.method="edgeR",
                         iteration=3, FDR=0.05, floorPDEG=0.05)
  tcc <- estimateDE(tcc, test.method="edger", FDR=0.05)
}else if(type == "deseq2"){
  tcc <- calcNormFactors(tcc, norm.method="deseq2", test.method="deseq2",
                         iteration=3, FDR=0.05, floorPDEG=0.05)
  tcc <- estimateDE(tcc, test.method="deseq2", FDR=0.05)
}
#------------------------------------------------------------------------------#
NormCount <- as.data.frame(getNormalizedData(tcc))
NormCount <- NormCount %>%
  mutate(ID = rownames(NormCount)) %>%
  select(ID, everything())

NormCount <- merge(NormCount, data.frame(ID = Gene$ID, GeneSymbol = Gene$GeneSymbol), by = "ID")

NormCount <- NormCount %>%
  select(ID, GeneSymbol, everything())
#------------------------------------------------------------------------------#
DEG <- as.data.frame(getResult(tcc, sort=TRUE))
DEG <- merge(DEG, data.frame(gene_id = Gene$ID, GeneSymbol = Gene$GeneSymbol), by = "gene_id")

DEG <- DEG %>%
  select(gene_id, GeneSymbol, everything())
DEG <- DEG[order(DEG$rank), ]
DEG$CustomedDEG <- ifelse(DEG$p.value < 0.05 & DEG$m.value < -1, "CR",
                  ifelse(DEG$p.value < 0.05 & DEG$m.value > 1, "NR","None"))
#------------------------------------------------------------------------------#
write.xlsx(DEG, "/labmed/01.AML/240123.AML.2_5_6_15.DEG.xlsx", sheetName='RNA_DEG_2_5_6_15_New', append=TRUE)
#------------------------------------------------------------------------------#
Gene <- read.table('/media/src/hg19/00.RNA/hg19.GENCODE.v44.GeneLength.txt', 
                   sep='\t', 
                   col.names = c('ID', 'Type', 'GeneSymbol', 'Length'))
Gene <- list(ID=Gene$ID, GeneSymbol=Gene$GeneSymbol)
#------------------------------------------------------------------------------#
raw_count <- read_excel("/labmed/01.AML/240123.AML.Total.Info.xlsx", sheet='RNA_ReadCount_New')
raw_count <- data.frame(raw_count)
rownames(raw_count) <- raw_count$ID
raw_count <- as.data.frame(raw_count[,-1:-2])
raw_count <- raw_count %>% select(-c('CR2', 'CR5', 'CR6', 'CR15'))
group <- rep(c('CR','NR'), c(4,5))
#------------------------------------------------------------------------------#  
tcc <- new("TCC", raw_count, group)
tcc <- filterLowCountGenes(tcc)
#------------------------------------------------------------------------------#
type <- "deseq2"
if (type == "edger"){
  tcc <- calcNormFactors(tcc, norm.method="tmm", test.method="edgeR",
                         iteration=3, FDR=0.05, floorPDEG=0.05)
  tcc <- estimateDE(tcc, test.method="edger", FDR=0.05)
}else if(type == "deseq2"){
  tcc <- calcNormFactors(tcc, norm.method="deseq2", test.method="deseq2",
                         iteration=3, FDR=0.05, floorPDEG=0.05)
  tcc <- estimateDE(tcc, test.method="deseq2", FDR=0.05)
}
#------------------------------------------------------------------------------#
NormCount <- as.data.frame(getNormalizedData(tcc))
NormCount <- NormCount %>%
  mutate(ID = rownames(NormCount)) %>%
  select(ID, everything())

NormCount <- merge(NormCount, data.frame(ID = Gene$ID, GeneSymbol = Gene$GeneSymbol), by = "ID")

NormCount <- NormCount %>%
  select(ID, GeneSymbol, everything())
#------------------------------------------------------------------------------#
DEG <- as.data.frame(getResult(tcc, sort=TRUE))
DEG <- merge(DEG, data.frame(gene_id = Gene$ID, GeneSymbol = Gene$GeneSymbol), by = "gene_id")

DEG <- DEG %>%
  select(gene_id, GeneSymbol, everything())
DEG <- DEG[order(DEG$rank), ]
DEG$CustomedDEG <- ifelse(DEG$p.value < 0.05 & DEG$m.value < -1, "CR",
                          ifelse(DEG$p.value < 0.05 & DEG$m.value > 1, "NR","None"))
#------------------------------------------------------------------------------#
write.xlsx(DEG, "/labmed/01.AML/240123.AML.1_3_10_13.DEG.xlsx", sheetName='RNA_DEG_1_3_10_13_New', append=TRUE)
#------------------------------------------------------------------------------#
Gene <- read.table('/media/src/hg19/00.RNA/hg19.GENCODE.v44.GeneLength.txt', 
                   sep='\t', 
                   col.names = c('ID', 'Type', 'GeneSymbol', 'Length'))
Gene <- list(ID=Gene$ID, GeneSymbol=Gene$GeneSymbol)
#------------------------------------------------------------------------------#
raw_count <- read_excel("/labmed/01.AML/240123.AML.Total.Info.xlsx", sheet='RNA_ReadCount_New')
raw_count <- data.frame(raw_count)
rownames(raw_count) <- raw_count$ID
raw_count <- as.data.frame(raw_count[,-1:-2])
raw_count <- raw_count %>% select(-c('NR1', 'NR5', 'NR8', 'NR9', 'NR13'))
group <- c(1,2,1,2,2,1,1,2)
#------------------------------------------------------------------------------#  
tcc <- new("TCC", raw_count, group)
tcc <- filterLowCountGenes(tcc)
#------------------------------------------------------------------------------#
type <- "deseq2"
if (type == "edger"){
  tcc <- calcNormFactors(tcc, norm.method="tmm", test.method="edgeR",
                         iteration=3, FDR=0.05, floorPDEG=0.05)
  tcc <- estimateDE(tcc, test.method="edger", FDR=0.05)
}else if(type == "deseq2"){
  tcc <- calcNormFactors(tcc, norm.method="deseq2", test.method="deseq2",
                         iteration=3, FDR=0.05, floorPDEG=0.05)
  tcc <- estimateDE(tcc, test.method="deseq2", FDR=0.05)
}
#------------------------------------------------------------------------------#
NormCount <- as.data.frame(getNormalizedData(tcc))
NormCount <- NormCount %>%
  mutate(ID = rownames(NormCount)) %>%
  select(ID, everything())

NormCount <- merge(NormCount, data.frame(ID = Gene$ID, GeneSymbol = Gene$GeneSymbol), by = "ID")

NormCount <- NormCount %>%
  select(ID, GeneSymbol, everything())
#------------------------------------------------------------------------------#
DEG <- as.data.frame(getResult(tcc, sort=TRUE))
DEG <- merge(DEG, data.frame(gene_id = Gene$ID, GeneSymbol = Gene$GeneSymbol), by = "gene_id")

DEG <- DEG %>%
  select(gene_id, GeneSymbol, everything())
DEG <- DEG[order(DEG$rank), ]
DEG$CustomedDEG <- ifelse(DEG$p.value < 0.05 & DEG$m.value < -1, "131013",
                          ifelse(DEG$p.value < 0.05 & DEG$m.value > 1, "25615","None"))
#------------------------------------------------------------------------------#
write.xlsx(DEG, "/labmed/01.AML/240123.AML.CR_vs_CR.DEG.xlsx", sheetName='RNA_DEG_CR_vs_CR', append=TRUE)
#------------------------------------------------------------------------------#
