library(ggplot2)
library(smplot2)
#------------------------------------------------------------------------------#
setwd('/labmed/02.AML/08.GSE163522/02.Methylkit/04.FDR/01.TF')
#------------------------------------------------------------------------------#
TF_list <- read.table('/labmed/02.AML/08.GSE163522/02.Methylkit/04.FDR/01.TF/TF_list.tsv', sep='\t', header=T)
for (TF in TF_list$GeneSymbol){
  Pearson_data <- read.table(paste0('/labmed/02.AML/08.GSE163522/02.Methylkit/04.FDR/01.TF/', TF, '.pearson.tsv'),
                             sep='\t',
                             header=TRUE)
  Pearson_data$Expression <- log(Pearson_data$Expression, 10)
  # Pearson_data$Expression <- Pearson_data$Expression * 1000000
  #------------------------------------------------------------------------------#
  Plot <- ggplot(Pearson_data, aes(x=Methylation, y=Expression)) +
    geom_point(pch=1, colour='blue', fill = 'white', size =2, stroke = 2) +
    theme_bw() +
    xlab('DNA methylation (TF binding site)') + 
    ylab('Gene expression (TPM)') +
    sm_statCorr(color = 'black', 
                corr_method = 'pearson',
                linetype = 'dashed',
                separate_by='\n',
                text_size = 4.5,
                label_x=max(Pearson_data$Methylation)- 0.1,
                label_y=min(Pearson_data$Expression) + 0.2) +
    annotate("text", x=max(Pearson_data$Methylation)-0.05, y=max(Pearson_data$Expression), label= TF, size=4.5) + 
    theme(panel.grid.major = element_blank(),
          panel.grid.minor = element_blank(),
          axis.title.x = element_text(margin = margin(t = 10,b=5), size=13),
          axis.title.y = element_text(margin = margin(r = 10,l=5), size=13))
  #------------------------------------------------------------------------------#
  ggsave(paste0('Figure3C.', TF, '.pdf'),
         plot=Plot,
         height=5, width=5)
  #------------------------------------------------------------------------------#
}
