library(ggbiplot)
library(ggplot2)
library(gridExtra)
library(cowplot)
#------------------------------------------------------------------------#
Table <- read.table('/labmed/06.AML/Result/00.Tables/Methylkit.Annotation.txt',header=T, sep='\t')
Match <- read.table('/media/src/hg19/01.Methylation/00.Bed/HGMD.Gene.bed',header=F, sep='\t')
Table <- subset(Table, Table$annot.symbol %in% Match$V4)
#------------------------------------------------------------------------#
Plot <- function(Data, x_axis, fill_color, group, Gene){
  date <- format(Sys.Date(), "%y%m%d")
  filename <- sprintf("/labmed/00.Code/00.Methylation/02.Plot/%s.Gene.%s.comp.pdf", Gene, group)
  
  actual_categories <- group
  color_mapping <- c('CR' = 'tan1', 'NR' = 'lightskyblue', 'Normal' = 'lightsteelblue4')
  
  Tx <- read.table('/media/src/hg19/01.Methylation/00.Bed/Exon.Intron.bed')
  colnames(Tx) <- c('Chromosome', 'Start' ,'End', 'GeneSymbol', 'Region', 'Strand')
  Table <- subset(Tx, Tx$GeneSymbol == Gene)
  Table['Color'] = ifelse(Table$Region=='exon', "black", "gray")
  Table['Size'] = ifelse(Table$Region=='exon', 1, 0.5)
  
  p1 <- ggplot(Data, aes_string(x = "End", y = x_axis)) +
    geom_point(aes(fill = Group), alpha = 0.9, shape = 21, size=2.5, stroke=0.7) +
    geom_smooth(method = "loess", se = FALSE, color='red', size = 0.2, span=0.35) +
    scale_fill_manual(values = color_mapping, breaks = actual_categories) +
    scale_color_manual(values = color_mapping, breaks = actual_categories) +
    ggtitle(Gene) +
    xlab('') +
    ylab('Percent Methylation') +
    xlim(Data[1,3], Data[nrow(Data), 3]) + 
    ylim(0, 100) +
    theme_bw() +
    theme(panel.grid.major = element_blank(), 
          panel.grid.minor = element_blank(),
          plot.title = element_text(size=10, hjust=0.5, face='italic'),
          axis.title = element_text(size = 10),
          axis.text=element_text(color="black"), 
          axis.ticks=element_line(color="black"),
          axis.text.x=element_text(size=7, angle=0, hjust=0.5, vjust=1))
#------------------------------------------------------------------------#
  p2 <- ggplot(Table) +
    geom_segment(aes(x = Start, xend = End,
                     y = 4, yend = 4,
                     colour = Color, size= Size)) +
    scale_color_manual(values = c("gray30", 'gray30'), 
                       labels = c("exon", "intron")) + 
    ylim(0,5) +
    xlab('') + ylab('Percent') +
    xlim(Data[1,3], Data[nrow(Data), 3]) +
    theme_bw() +
    theme(panel.background = element_blank(),
          panel.border = element_blank(),
          panel.grid.major = element_blank(),
          panel.grid.minor = element_blank(),
          axis.text.x = element_blank(),
          axis.title.x = element_blank(),
          axis.text.y = element_blank(),
          axis.title.y = element_blank(),
          axis.ticks.x = element_blank(),
          axis.ticks.y = element_blank(),
          legend.background = element_blank(),
          legend.position = "none",
          legend.key = element_blank(),
          legend.text = element_blank(),
          legend.title = element_blank())

  if (Table$Strand[1] == "-"){
    p2 <- p2 + 
      annotate(geom = "segment",
               x=Table$End[nrow(Table)], y=2, 
               xend=Table$End[nrow(Table)] - (Table$End[nrow(Table)] - Table$End[1])/3, yend = 2,
               arrow = arrow(type = "open", length = unit(0.1, "inches")),
               color='gray', size=1)
  } else {
    p2 <-  p2 + 
      annotate(geom = "segment",
             x=Table$Start[1], y=2, 
             xend=Table$Start[1] + (Table$Start[nrow(Table)] - Table$Start[1])/3, yend = 2,
             arrow = arrow(type = "open", length = unit(0.1, "inches")),
             color='gray', size=1) 
  }
  
  p <- p1 + p2 +
    plot_layout(ncol = 1, heights = c(3, 1))
  
  ggsave(p, file = filename, height = 6, width = 11, scale = 0.55)
}

#------------------------------------------------------------------------#
for (GENE in Table$Gene){
  Genes <- GENE
  date <- format(Sys.Date(), "%y%m%d")
  Meth_CR <- read.table(sprintf('Result/01.Plots/AML.%s.Case.CR.avg.txt', Genes), header=T, sep='\t')
  Meth_NR <- read.table(sprintf('Result/01.Plots/AML.%s.Case.NR.avg.txt', Genes), header=T, sep='\t')
#   Meth_Norm <- read.table(sprintf('Result/01.Plots/AML.%s.Normal.avg.txt', Genes), header=T, sep='\t')
  
  Plot(Data = Meth_CR, x_axis = 'Meth_CR', fill_color = 'tan1', group = 'CR', Gene = Genes)
  Plot(Data = Meth_NR, x_axis = 'Meth_NR', fill_color = 'lightskyblue', group = 'NR', Gene = Genes)
#   Plot(Data = Meth_Norm, x_axis = 'Meth_Normal', fill_color = 'lightsteelblue4', group = 'Normal', Gene = Genes)
}