library(gplots)
library(RColorBrewer)
library(dplyr)
library(ggplot2)
library(ggbiplot)
library(ggrepel)
#------------------------------------------------------------------------#
args <- commandArgs(trailingOnly = TRUE)
Group_A <- args[1]
Group_B <- args[2]
Number_A <- args[3]
Number_B <- args[4]
#------------------------------------------------------------------------#
Data_list <- list.files('Result/00.Tables')

exclude_strings <- c("Table", "CpG.Merged", "2kb")
Data_list <- Data_list[!grepl(paste(exclude_strings, collapse = "|"), Data_list)]
#------------------------------------------------------------------------#
#데이터 호출 및 가공
for (data in Data_list){
    Prefix <- unlist(strsplit(data, "\\."))
    Prefix <- Prefix[3]
    
    Data <- read.table(paste0('Result/00.Tables/', data), header=T, sep='\t')
    Data <- Data[,c(-1,-2,-3)]
    Data <- Data[complete.cases(Data),]
    
    pca_res <- prcomp(t(Data))
    
    samp_colors <- c("tan1", "lightskyblue") 
    names(samp_colors) <- c(Group_A, Group_B)
    
    samp_data <- data.frame(
        "GROUP" = rep(c(Group_A, Group_B),c(Number_A, Number_B)),
        row.names = colnames(Data))
        
    PCA <- ggbiplot(pca_res, ellipse = T, 
    var.axes = F, obs.scale = 1, var.scale = 1) +
    geom_point(aes(fill = samp_data$GROUP), size = 5, shape=21, stroke=1) +
    scale_color_manual(values = c("tan1", "lightskyblue"), 
                        labels = c(Group_A, Group_B)) +
    scale_fill_manual(values = c("tan1", "lightskyblue"), 
                        labels = c(Group_A, Group_B)) +
    ggtitle(paste0("PCA of ", Prefix)) +
    # coord_fixed(ratio = 1) +
    theme_test() +
    theme(axis.title = element_text(size = 20),
          axis.ticks.x=element_blank(),
          axis.text.x=element_blank(),
          axis.ticks.y=element_blank(),
          axis.text.y=element_blank(),
          plot.title = element_text(size = 22, hjust = 0.5),
          legend.text = element_text(size = 16),
          legend.title = element_blank(),
          legend.position = "top")

    ggsave(PCA, file=paste0('Result/01.Plots/', 'PCA.', Prefix, '.pdf'))
}