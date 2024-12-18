library(gplots)
library(RColorBrewer)
library(dplyr)
library(pheatmap)
#------------------------------------------------------------------------#
args <- commandArgs(trailingOnly = TRUE)
Group_A <- args[1]
Group_B <- args[2]
Number_A <- args[3]
Number_B <- args[4]
#------------------------------------------------------------------------#
current_date <- Sys.Date()
Date <- format(current_date, "%y%m%d")
#------------------------------------------------------------------------#
Data <- read.table('Result/00.Tables/230825.Methyl.DMR.Personal.txt', header=T)
Data <- Data[complete.cases(Data),]
Heatmap.Data <- Data[,4:ncol(Data)]

Heatmap.Data <- as.data.frame(lapply(Heatmap.Data, as.numeric))
Heatmap.Data <- as.matrix(Heatmap.Data)
#------------------------------------------------------------------------#
samp_colors <- c("tan1", "lightskyblue") 
names(samp_colors) <- c(Group_A, Group_B)

samp_data <- data.frame(
  "Group" = rep(c(Group_A, Group_B), c(12,12)),
  row.names = colnames(Data[4:ncol(Data)])
)
#------------------------------------------------------------------------#
pdf(paste0('Result/01.Plots/', 'Heatmap.DMR.pdf'), width=15, height=15)
pheatmap(mat = Heatmap.Data,
         color = colorRampPalette(c("blue", "yellow"))(100),
         annotation_col = samp_data,
         annotation_colors = list("Group" = samp_colors),
         clustering_method = 'average',
         show_rownames = F, 
         show_colnames = F,
         cluster_rows = T,
         cluster_cols = T,
         clustering_distance_rows = "correlation",
         scale = "row",
         main = 'Differentially methylated Region Heatmap',
         cellwidth = 20)
dev.off()
