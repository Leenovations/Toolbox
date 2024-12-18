library(ggplot2)
library(cowplot)
library(ggbiplot)
library(gridExtra)
library(patchwork)
library(GenomicRanges)
library(ggpubr)
library(openxlsx)

Gene <- c('TAL1', 'BCL11A', 'GATA1', 'GATA2', 'NFE2', 'TLR1', 'TLR2', 'TLR3', 'TLR4', 'TLR5', 'TLR6', 'TLR7', 'TLR8', 'CD8A', 'CD8B', 'CTLA4')
DMR_Data <- read.xlsx('/labmed/01.AML/240123.AML.Total.Info.xlsx', sheet='Methylkit')

for (gene in Gene){
  data <- read.table(paste0('/labmed/01.AML/01.WGBS/240119.AML.150bp.', gene, '.Methyl.txt'),
                     sep='\t',
                     header=TRUE)
  
  data$color <- ifelse(data$CR.NR > 0, 'tan1', 'lightskyblue')
  #---------------------------------------------------------------------------------------------------------#
  CR <- ggplot(data, aes(x = Start, y = CR)) +
    geom_bar(fill = 'tan1',
             color=NA,
             stat = "identity", 
             position = "identity", 
             width = 150) +
    theme_classic() +
    xlab('') + 
    ylab('') + 
    ggtitle(paste0('', '\n'), subtitle='CR') +
    scale_y_continuous(breaks = c(0, 100), labels=c(0, 100)) + 
    theme(axis.line.x = element_blank(),
          panel.grid.major = element_blank(),
          panel.grid.minor = element_blank(),
          axis.title.y = element_text(size=10),
          plot.subtitle = element_text(size=10, hjust=0.5, face = c('bold')),
          plot.title = element_text(size=15, hjust=0.5, face = c('bold.italic')),
          axis.title = element_text(size = 10),
          axis.text=element_text(color="black"),
          axis.ticks.x=element_blank(),
          axis.text.x=element_blank()) +
    coord_cartesian(ylim = c(0 ,100), expand = T, clip = "off")
  #---------------------------------------------------------------------------------------------------------#
  NR <- ggplot(data, aes(x = Start, y = NR)) +
    geom_bar(fill = 'lightskyblue',
             color=NA,
             stat = "identity", 
             position = "identity", 
             width = 150) +
    theme_classic() +
    xlab('') + 
    ylab('') + 
    ggtitle('NR') + 
    scale_y_continuous(breaks = c(0, 100), labels=c(0, 100)) + 
    theme(axis.line.x = element_blank(),
          panel.grid.major = element_blank(),
          panel.grid.minor = element_blank(),
          axis.title.y = element_text(size=10),
          plot.title = element_text(size=10, hjust=0.5, face = c('bold')),
          axis.title = element_text(size = 10),
          axis.text=element_text(color="black"),
          axis.ticks.x=element_blank(),
          axis.text.x=element_blank()) + 
    coord_cartesian(ylim = c(0 ,100), expand = T, clip = "off")
  #---------------------------------------------------------------------------------------------------------#
  Data_sub <- subset(DMR_Data, DMR_Data$annot.symbol==gene)
  Range <- unique(Data_sub[,c('start', 'end')])
  #---------------------------------------------------------------------------------------------------------#
  bed1 <- read.table("/media/src/hg19/01.Methylation/00.Bed/CGI.bed", header = FALSE, col.names = c("chromosome", "start", "end"))
  bed2 <- read.table("/media/src/hg19/01.Methylation/00.Bed/NCBI.RefSeq.Selected.Gene.bed", header = FALSE, col.names = c("chromosome", "start", "end", "genesymbol", "strand"))
  bed2 <- subset(bed2, bed2$genesymbol==gene)
  gr1 <- GRanges(seqnames = bed1$chromosome, ranges = IRanges(start = bed1$start, end = bed1$end))
  gr2 <- GRanges(seqnames = bed2$chromosome, ranges = IRanges(start = bed2$start, end = bed2$end))
  overlap <- findOverlaps(gr2, gr1)
  CpG_island_table <- data.frame('Start'=bed1[overlap@to,]$start,
                                 'End'=bed1[overlap@to,]$end)
  #---------------------------------------------------------------------------------------------------------#
  Tx <- read.table('/media/src/hg19/01.Methylation/00.Bed/NCBI.RefSeq.Selected.Exon.Intron.None.bed', sep='\t')
  colnames(Tx) <- c('Chromosome', 'Start' ,'End', 'GeneSymbol', 'Region', 'Strand')
  Exon <- subset(Tx, Tx$GeneSymbol == gene & Tx$Region == 'exon')
  Intron <- subset(Tx, Tx$GeneSymbol == gene & Tx$Region == 'intron')
  #---------------------------------------------------------------------------------------------------------#
  CR_NR <- ggplot(data, aes(x = Start, y = CR-NR)) +
    geom_bar(fill = data$color,
             color=NA,
             stat = "identity", 
             position = "identity", 
             width = 150) + 
    theme_classic() +
    xlab('') + 
    ylab('') + 
    ggtitle('CR vs NR') + 
    scale_y_continuous(breaks = c(-50, 50), labels=c(-50, 50)) + 
    geom_hline(yintercept = 0,
               linetype='solid',
               color='black',
               alpha=0.3,
               size=0.1) + 
    theme(plot.margin = unit(c(0, 0, 2, 0), "cm"),
          axis.line.x = element_blank(),
          panel.grid.major = element_blank(),
          panel.grid.minor = element_blank(),
          axis.title.y = element_text(size=10),
          plot.title = element_text(size=10, hjust=0.5, face = c('bold')),
          axis.title = element_text(size = 10),
          axis.text=element_text(color="black"),
          axis.ticks.x=element_blank(),
          axis.text.x=element_blank()) +
    annotate(geom = "text", x = median(c(data$Start[1], data$End[nrow(data)])), y = -70, label = "DMR", size = 2, fontface=2) +
    annotate(geom = "rect", xmin=Range$start, xmax=Range$end, ymin=-80 , ymax=-95, color="blueviolet", fill='blueviolet') +
    annotate(geom = "text", x = median(c(data$Start[1], data$End[nrow(data)])), y = -110, label = "CpG island", size = 2, fontface=2) +
    annotate(geom = "rect", xmin=CpG_island_table$Start, xmax=CpG_island_table$End, ymin=-120 , ymax=-135, color="darkgreen", fill='darkgreen') +
    annotate(geom = "text", x = median(c(data$Start[1], data$End[nrow(data)])), y = -150, label = "Exon/Intron", size = 2, fontface=2) +
    annotate(geom = "rect", xmin=Exon$Start, xmax=Exon$End, ymin=-160 , ymax=-180, color="navy", fill='navy') +
    annotate(geom = "rect", xmin=Intron$Start, xmax=Intron$End, ymin=-169 , ymax=-171, color="navy", fill='navy') +
    coord_cartesian(ylim = c(-50, 50), expand = T, clip = "off")
  #---------------------------------------------------------------------------------------------------------#
  Data <- read.xlsx('/labmed/01.AML/240123.AML.Total.Info.xlsx', sheet='RNA_TPM')
  Data <- Data[-1]

  Sub_Data <- subset(Data, Data$GeneSymbol == gene)
  Sub_Data <- Sub_Data[-1]
  Trans_Data <- t(Sub_Data)
  Trans_Data <- as.data.frame(Trans_Data)
  colnames(Trans_Data) <- c('TPM')
  Trans_Data$Group <- rep(c('CR', 'NR'), c(8, 5))
  Trans_Data$TPM <- log10(Trans_Data$TPM)

  Barplot <- ggboxplot(Trans_Data, 
                       x = "Group", 
                       y = "TPM", 
                       fill = "Group", 
                       palette = c("tan1", "lightskyblue"), 
                       width = 0.3,
                       outlier.shape = NA) + 
    ylab(log[10]~TPM) +
    scale_x_discrete(limits = c("NR", "CR")) +
    coord_flip() +
    theme(plot.margin = margin(2.5, 1, 2.5, 1, "cm"),
          axis.text.x = element_text(size=8),
          axis.text.y = element_text(size=8),
          axis.title.x = element_text(size=10, face='bold'),
          axis.title.y = element_blank(),
          legend.position = "none",
          legend.key = element_blank(),
          legend.text = element_blank(),
          legend.title = element_blank())
  #---------------------------------------------------------------------------------------------------------#
      Methyl <- CR + NR + CR_NR + plot_layout(ncol = 1)
      Plot <- plot_grid(Methyl, Barplot)

  Merged_plot <- ggdraw() +
    draw_plot(Plot) +
    draw_label(gene, size = 13, x = 0.5, y = 0.93, fontface = "bold.italic")
  #---------------------------------------------------------------------------------------------------------#
  ggsave(paste0('/labmed/01.AML/04.Results/00.Plots/', gene, '.Exon.Bar.anno.png'),
         height=5,
         plot=Merged_plot)
}