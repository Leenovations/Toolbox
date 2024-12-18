library(ggplot2)
library(readxl)
library(pheatmap)
library(RColorBrewer)
#--------------------------------------------------------------------------------#
setwd('/labmed/01.AML/')
#--------------------------------------------------------------------------------#
Name <- read_excel('/labmed/01.AML/240123.AML.Total.Info.xlsx', sheet = 'Sample_Call')
#--------------------------------------------------------------------------------#
Pathway <- list.files('/labmed/01.AML/01.WGBS/02.Gene.Methyl/', '_')
Pathway <- strsplit(Pathway, '\\.')
Pathway <- sapply(Pathway, function(x) x[1])
#--------------------------------------------------------------------------------#
for (pathway in Pathway){
  Sample <- data.frame(sample=na.omit(Name$WGBS))
  GO <- list.files('/labmed/01.AML/01.WGBS/02.Gene.Methyl/', pathway)
  for (go in GO){
    Header <- strsplit(go, '\\.')
    Header <- sapply(Header, function(x) x[2])
    Data <- read.table(paste0('/labmed/01.AML/01.WGBS/02.Gene.Methyl/', go), 
                       sep='\t', 
                       header = T,
                       col.names=Header)
    Sample <- cbind(Sample, Data)
  }
  rownames(Sample) <- as.character(Sample[, 1])
  Sample <- Sample[,-1]
  CR <- Sample[1:12,]
  NR <- as.data.frame(t(colMeans(Sample[13:24,])))

  Diff <- data.frame(
    CpGIShelf = CR$CpGIShelf - NR$CpGIShelf,
    CpGIShore = CR$CpGIShore - NR$CpGIShore,
    CpGIsland = CR$CpGIsland - NR$CpGIsland,
    Enhancer = CR$Enhancer - NR$Enhancer,
    Exon = CR$Exon - NR$Exon,
    Intron = CR$Intron - NR$Intron,
    Promoter = CR$Promoter - NR$Promoter)

  rownames(Diff) <- paste0(rownames(Sample)[1:12], ' vs NR')
  Heatmap <- pheatmap(Diff,
                      color =  colorRampPalette(rev(RColorBrewer::brewer.pal(n = 10, name ="RdYlGn")))(100),
                      legend_breaks = c(-1.5,1.5),
                      legend_labels = c("Low", "High"),
                      border_color = NA,
                      row_names_side = "left",
                      clustering_method = 'average',
                      show_rownames = T,
                      show_colnames = T,
                      treeheight_row = 0,
                      clustering_distance_rows = "correlation",
                      cluster_rows = T,
                      cluster_cols = T,
                      display_numbers = TRUE,
                      fontsize_number = 10,
                      scale = "row",
                      main = paste0(gsub('_', ' ', pathway), '\n'))

  png(paste0('/labmed/01.AML/04.Results/00.Plots/', pathway, ".heatmap.png"), width = 2000, height = 2000, units = "px",res = 300)
  print(Heatmap)
  dev.off()
}
#--------------------------------------------------------------------------------#