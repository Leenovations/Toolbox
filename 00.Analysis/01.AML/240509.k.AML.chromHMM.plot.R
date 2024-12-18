library(ggbiplot)
library(ggplot2)
library(gridExtra)
library(cowplot)
library(patchwork)
#------------------------------------------------------------------------------#
setwd('/labmed/02.AML/08.GSE163522/02.Methylkit/04.FDR/00.Genebinbed')
Input <- read.table('/labmed/02.AML/08.GSE163522/02.Methylkit/04.FDR/00.Genebinbed/BCL11A.input.txt',
                    sep='\t',
                    header=T)
Input <- cbind(Input[,1:3], Input[,4:6]/100)
#------------------------------------------------------------------------------#
spline_CR <- abs(as.data.frame(spline(Input$End, Input$CR)))
colnames(spline_CR) <- c('End','CR')
spline_NR <- abs(as.data.frame(spline(Input$End, Input$NR)))
colnames(spline_NR) <- c('End','NR')
spline_Normal <- abs(as.data.frame(spline(Input$End, Input$Normal)))
colnames(spline_Normal) <- c('End','Normal')
#------------------------------------------------------------------------------#
p1 <- ggplot() +
  geom_line(data = spline_CR,  aes(x = End, y = CR, colour='CR'), size=1) +
  geom_line(data = spline_NR,  aes(x = End, y = NR, colour='NR'), size=1) +
  geom_line(data = spline_Normal,  aes(x = End, y = Normal, colour='Normal'), size=1) +
  scale_color_manual(values = c('forestgreen',"royalblue4","firebrick1")) +
  xlim(60684328, 60794779) + 
  xlab('') +
  ylab('DNA\nmethylation\n (WGBS)') +
  scale_y_continuous(expand = c(0.01, 0.01), breaks = c(0,1), labels = c(0,1)) +
  scale_x_continuous(expand = c(0,0)) +
  theme_classic() +
  theme(panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        plot.title = element_blank(),
        axis.title = element_text(size = 10),
        axis.title.y = element_text(angle = 0, vjust = 0.5, hjust=0.5),
        axis.text=element_text(color="black"), 
        axis.ticks=element_blank(),
        axis.text.x=element_blank(),
        legend.title = element_blank(),
        legend.position = "right")
#------------------------------------------------------------------------------#
ExonIntron <- read.table('BCL11A.Geneinfo.txt',sep='\t', header=FALSE, col.names=c('Chr','Start','End','Strand','Gene','NM','Region'))
ExonIntron <- ExonIntron[c(-2, -9, -10),]
ExonIntron$Region <- gsub("Intron_\\d+", "Intron", ExonIntron$Region)
ExonIntron$Region <- gsub("Exon_\\d+", "Exon", ExonIntron$Region)
ExonIntron['Color'] = ifelse(ExonIntron$Region=='Exon', "black", "gray")
ExonIntron['Size'] = ifelse(ExonIntron$Region=='Exon', 1, 0.5)
#------------------------------------------------------------------------------#
p2 <- ggplot(ExonIntron) +
  geom_segment(aes(x = Start, xend = End,
                   y = 1, yend = 1,
                   colour = Color, size= Size)) +
  scale_color_manual(values = c("navy", 'navy'), 
                     labels = c("Exon", "Intron")) + 
  xlim(60684328, 60794779) + 
  ylim(1,1) +
  xlab('') + 
  ylab('NM_022893.4') +
  ggtitle('BCL11A') +
  theme_bw() +
  theme(panel.background = element_blank(),
        panel.border = element_blank(),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        plot.title = element_text(size=10, hjust=0.5, face='italic'),
        axis.text.x = element_blank(),
        axis.title.x = element_blank(),
        axis.title.y = element_text(angle = 0, vjust = 0.5, hjust=0.5),
        axis.text.y = element_blank(),
        axis.ticks.x = element_blank(),
        axis.ticks.y = element_blank(),
        legend.background = element_blank(),
        legend.position = "none",
        legend.key = element_blank(),
        legend.text = element_blank(),
        legend.title = element_blank())
#------------------------------------------------------------------------------#
HMM <- read.table('BCL11A.HMM.txt',sep='\t', header=FALSE, col.names=c('Chr','Start','End','Strand','Gene','NM','Region'))
HMM['Size'] = 1
#------------------------------------------------------------------------------#
p3 <- ggplot(HMM) +
  geom_segment(aes(x = Start, xend = End,
                   y = 1, yend = 1,
                   colour = Region, 
                   size= Size)) +
  scale_color_manual(values = c("seagreen", 'tomato','red','greenyellow','hotpink1','lightgoldenrod')) +
  guides(size = "none", color = guide_legend(override.aes = list(linewidth = 6))) +
  xlim(60684328, 60794779) + 
  ylim(1,1) +
  xlab('') + 
  ylab('K562\nChromHMM') +
  theme_bw() +
  guides(size = F) +
  theme(panel.background = element_blank(),
        panel.border = element_blank(),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        axis.text.x = element_blank(),
        axis.title.x = element_blank(),
        axis.title.y = element_text(angle = 0, vjust = 0.5, hjust=0.5),
        axis.text.y = element_blank(),
        axis.ticks.x = element_blank(),
        axis.ticks.y = element_blank(),
        legend.background = element_blank(),
        legend.title = element_blank(),
        legend.position = "bottom")
#------------------------------------------------------------------------------#
p <- p2 + p1 + p3 +
  plot_layout(ncol = 1, heights = c(2, 15, 2))
ggsave(p, file='BCL11A.HMM.pdf', width=10, height=4)
#------------------------------------------------------------------------------#
p
#------------------------------------------------------------------------------#
