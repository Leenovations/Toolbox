library(ggplot2)
library(readxl)
library(patchwork)
library(viridis)
#---------------------------------------------------------------------#
Gain <- read.table('/labmed/06.BPDCN/Cytoband.Gain.prcd.txt', sep='\t', header = F, col.names = c('locus', 'Freq', 'type'))
Loss <- read.table('/labmed/06.BPDCN/Cytoband.Loss.prcd.txt', sep='\t', header = F, col.names = c('locus', 'Freq', 'type'))
Loss <- subset(Loss, Loss$Freq>2)
#---------------------------------------------------------------------#
CNV_Gain <- ggplot(Gain, aes(x=reorder(locus, -Freq), y=Freq)) +
  geom_bar(stat = "identity",
           position = "identity",
           fill='brown2') +
  theme_classic() +
  xlab('') +
  ylab('\nNo. of CNAs\n') +
  scale_y_continuous(expand = c(0,0), breaks = c(0, 1, 2), label=c(0,1,2)) +
  ggtitle('Chromosomal Copy Number Gain\n') +
  theme(plot.margin = unit(c(2,2,2,2), 'cm'),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        plot.title = element_text(size=10, hjust=0.5, face = c('bold')),
        plot.subtitle = element_text(size=10, hjust=0.5),
        axis.title = element_text(size = 10, face='bold'),
        legend.position = "none",
        axis.text.x = element_text(size=8, face='bold', angle = 90, vjust = 0.5),
        axis.text=element_text(color="black"))

ggsave('BPDCN.Chromosomal.CNV.prcd.Gain.freq.png', height=4, width=10,
       plot=CNV_Gain)
#------------------------------------------------------------------------------#
CNV_Loss <- ggplot(Loss, aes(x=reorder(locus, -Freq), y=Freq)) +
  geom_bar(stat = "identity",
           position = "identity",
           fill='blue4') +
  theme_classic() +
  xlab('') +
  ylab('\nNo. of CNAs\n') +
  scale_y_continuous(expand = c(0,0)) +
  ggtitle('Chromosomal Copy Number Loss\n') +
  theme(plot.margin = unit(c(0,0.5,2,0.5), 'cm'),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        plot.title = element_text(size=10, hjust=0.5, face = c('bold')),
        plot.subtitle = element_text(size=10, hjust=0.5),
        axis.title = element_text(size = 10, face='bold'),
        legend.position = "none",
        axis.text.x = element_text(size=8, face='bold', angle = 90, vjust = 0.5),
        axis.text=element_text(color="black"))

ggsave('BPDCN.Chromosomal.CNV.Loss.freq.png', height=4, width=10,
       plot=CNV_Loss)
#------------------------------------------------------------------------------#
Total <- CNV_Gain + CNV_Loss + plot_layout(ncol = 1)
ggsave('ChromosomalCNV.png',
       plot=Total, width=13)
ggsave('ChromosomalCNV.pdf',
       plot=Total, width=13)
