library(methylKit)
library(genomation)
library(annotatr)
library(dplyr)
library(openxlsx)
#------------------------------------------------------------------------------
args <- commandArgs(trailingOnly = TRUE)
Core <- as.numeric(args[1])
Group_1 <- as.numeric(args[2])
Group_2 <- as.numeric(args[3])
#------------------------------------------------------------------------------
current_date <- Sys.Date()
Date <- format(current_date, "%y%m%d")
#------------------------------------------------------------------------------#
files <- list.files(paste0(getwd(), '/CpG/'))
pattern <- 'cov'
matching_files <- paste0(getwd(), '/CpG/', grep(pattern, files, value=TRUE))
#------------------------------------------------------------------------------#
Input <- list()
for (i in 1:length(matching_files)){
  Input[[i]] <- matching_files[i]
}
#------------------------------------------------------------------------------#
sample.id <- strsplit(files, '.deduplicated')
sample.id <- unlist(sample.id)[seq(from = 1, to = length(sample.id)*2, by = 2)]
ID <- list()
for (i in 1:length(sample.id)){
  ID[[i]] <- sample.id[i]
}
#------------------------------------------------------------------------------#
#Methylkit Run
Data <- methRead(Input,
                 sample.id = ID,
                 assembly = 'hg19',
                 treatment=rep(c(0,1),c(Group_1, Group_2)),
                 context='CpG',
                 mincov=1,
                 resolution='region',
                 pipeline='bismarkCoverage')
#------------------------------------------------------------------------------#
new_directory <- 'Result/01.Plots/'

if (!file.exists(new_directory)) {
  dir.create(new_directory)
} else {
  cat("Directory already exists. Skipping directory creation.")
}
#------------------------------------------------------------------------------#
pdf(paste0(new_directory, 'Methylkit.pdf'))
for (i in 1:length(sample.id)){
  getMethylationStats(Data[[i]],
                      plot = TRUE,both.strands=FALSE)
  getCoverageStats(Data[[i]],
                   plot = TRUE,both.strands=FALSE)
}
dev.off()
#------------------------------------------------------------------------------#
normalizedData <- normalizeCoverage(Data,
                                    method="median",
                                    chunk.size = 1e8)
cat("\n \033[31mNormalization completed\033[0m\n \n")
#------------------------------------------------------------------------------#
FilteredData <- filterByCoverage(normalizedData, 
                                 lo.count=NULL,
                                 lo.perc=NULL,
                                 hi.count=NULL, 
                                 hi.perc=NULL,
                                 chunk.size = 1e8)
cat("\n \033[31mFiltration completed\033[0m\n \n")
#------------------------------------------------------------------------------#
MergedData <- unite(FilteredData, 
                    destrand = F,
                    chunk.size = 1e8,
                    mc.cores = Core,
                    save.db=F)
cat("\n \033[31mMerge complete\033[0m\n \n")
#------------------------------------------------------------------------------#
TiledData <- tileMethylCounts(MergedData, 
                             win.size=1000, 
                             step.size=1000, 
                             cov.bases=1,
                             mc.cores=Core)
cat("\n \033[31mTiling complete\033[0m\n \n")
#------------------------------------------------------------------------------#
DiffData <- calculateDiffMeth(TiledData,
                             mc.cores = Core,
                             chunk.size = 1e8,
                             effect='predicted',
                             weighted.mean = TRUE)
cat("\n \033[31mCalculation Diff complete\033[0m\n \n")
#------------------------------------------------------------------------------#
new_directory <- 'Result/00.Tables/'

if (!file.exists(new_directory)) {
  dir.create(new_directory)
} else {
  cat("Directory already exists. Skipping directory creation.\n")
}
#------------------------------------------------------------------------------#
Hyper <- getMethylDiff(DiffData, 
                      difference = 15,
                      qvalue = 0.05,
                      type = "hyper")

Hyper <- getData(Hyper)
Hyper <- data.frame(Hyper)
Hyper$DM_status <- 'hyper'

Hypo <- getMethylDiff(DiffData,
                      difference = 15, 
                      qvalue = 0.05, 
                      type = "hypo")

Hypo <- getData(Hypo)
Hypo <- data.frame(Hypo)
Hypo$DM_status <- 'hypo'
#------------------------------------------------------------------------------#
All <- rbind(Hyper, Hypo)
All <- All[, c('chr','start','end','DM_status', 'qvalue', 'strand','meth.diff')] 

write.table(All, paste0(new_directory, 'Methylkit.All.txt'),
            row.names = F, 
            col.names=F, 
            quote=F,
            sep='\t')
#------------------------------------------------------------------------------#
Diff = paste0(new_directory, 'Methylkit.All.txt')
extraCols = c(meth.diff = 'numeric')
dm_regions = read_regions(con = Diff,
                          genome = 'hg19', 
                          extraCols = extraCols, 
                          format = 'bed',
                          rename_name = 'DMR', 
                          rename_score = 'qvalue')

annots = c('hg19_cpgs', 'hg19_basicgenes', 'hg19_genes_intergenic',
           'hg19_genes_intronexonboundaries')
annotations = build_annotations(genome = 'hg19', annotations = annots)
dm_annotated = annotate_regions(regions = dm_regions,
                                annotations = annotations,
                                ignore.strand = TRUE,
                                quiet = FALSE)

df_dm_annotated = data.frame(dm_annotated)
write.table(df_dm_annotated,
            paste0(new_directory, 'Methylkit.Annotation.txt'),
            sep ='\t', quote = F, col.names = T)
#------------------------------------------------------------------------------#
Bed_hyper <- subset(df_dm_annotated, DMR=='hyper' & abs(meth.diff) >= 15)[1:3]
Bed_hyper <- unique(Bed_hyper)
colnames(Bed_hyper) <- c('Chromosome','Start','End')
write.table(Bed_hyper, 
            paste0('Result/02.Bed/',
                   'Hyper.DMR.bed'),
            sep='\t',
            quote=F,
            row.names=FALSE)

Bed_hypo <- subset(df_dm_annotated, DMR=='hypo' & abs(meth.diff) >= 15)[1:3]
Bed_hypo <- unique(Bed_hypo)
colnames(Bed_hypo) <- c('Chromosome','Start','End')
write.table(Bed_hypo, 
            paste0('Result/02.Bed/', 
                   'Hypo.DMR.bed'),
            sep='\t',
            quote=F,
            row.names=FALSE)
            
Bed_All <- df_dm_annotated[1:3]
Bed_All <- unique(Bed_All)
colnames(Bed_All) <- c('Chromosome','Start','End')
write.table(Bed_All, 
            paste0('Result/02.Bed/', 
                   'DMR.bed'),
            sep='\t',
            quote=F,
            row.names=FALSE)
#------------------------------------------------------------------------------#      
Promoter <- function(){
  Cutoff <- subset(df_dm_annotated, abs(meth.diff) >= 15)
  Data <- subset(Cutoff, annot.type == c("hg19_genes_promoters", "hg19_genes_5UTRs"))
  Gene_hyper <- unique(subset(Data, DMR=='hyper')$annot.symbol)
  Gene_hyper <- na.omit(Gene_hyper)
  Gene_hyper <- as.data.frame(Gene_hyper)
  Gene_Hypo <- unique(subset(Data, DMR=='hypo')$annot.symbol)
  Gene_Hypo <- na.omit(Gene_Hypo)
  Gene_Hypo <- as.data.frame(Gene_Hypo)
  xlsx <- createWorkbook()
  addWorksheet(xlsx, "Promoter_HyperMeth")
  writeData(xlsx,
            sheet = "Promoter_HyperMeth",
            Gene_hyper,
            startCol = 1,
            startRow = 1)
  saveWorkbook(xlsx,
               paste0(new_directory, 'Promoter.DMR.xlsx'),
               overwrite = TRUE)
  addWorksheet(xlsx, "Promoter_HypoMeth")
  writeData(xlsx,
            sheet = "Promoter_HypoMeth",
            Gene_Hypo,
            startCol = 1,
            startRow = 1)
  saveWorkbook(xlsx,
               paste0(new_directory,'Promoter.DMR.xlsx'),
               overwrite = TRUE)
}

Promoter()
#------------------------------------------------------------------------------#
Makexlsx <- function(level){
  Cutoff <- subset(df_dm_annotated, abs(meth.diff) >= 15)
  Data <- subset(Cutoff, DMR==level)
  xlsx <- createWorkbook()
  addWorksheet(xlsx, paste0(level,"Meth_All"))
  writeData(xlsx,
            sheet = paste0(level,"Meth_All"),
            Data,
            startCol = 1,
            startRow = 1)
  saveWorkbook(xlsx,
               paste0(new_directory, level ,'.DMR.xlsx'),
               overwrite = TRUE)
  for (region in unique(df_dm_annotated$annot.type)){
    Sub <- subset(Data, annot.type==region)
    addWorksheet(xlsx, region)
    writeData(xlsx,
              sheet = region,
              Sub,
              startCol = 1,
              startRow = 1)
    saveWorkbook(xlsx,
                 paste0(new_directory, level ,'.DMR.xlsx'),
                 overwrite = TRUE)
  }
}

Makexlsx("hyper")
Makexlsx("hypo")
