library(ggplot2)
library(readxl)
library(viridis)
#---------------------------------------------------------------------#
Freq.Data <- read_excel('~/Documents/03.NGS/05.GS/01.BPDCN/02.Table/240129.BPDCN.ChromosomeCNV.Freq.xlsx')
Freq.Data <- Freq.Data[,c('locus', 'Frequency')]
Freq.Data <- Freq.Data[order(-Freq.Data$Frequency), ]
Freq.Data <- subset(Freq.Data, Freq.Data$Frequency != 0)
Freq.Data$Group <- Freq.Data$Frequency
#---------------------------------------------------------------------#
Plot <- ggplot(Freq.Data, aes(x=reorder(locus, -Frequency), y=Frequency, fill=as.factor(Group))) +
  geom_bar(stat = "identity",
           position = "identity") +
  theme_classic() +
  xlab('') +
  ylab('\nFrequency\n') +
  scale_y_continuous(expand = c(0,0)) +
  scale_fill_viridis(discrete = TRUE) +  # Set YlGn color palette
  ggtitle('Chromosomal copy number frequency') +
  theme(plot.margin = unit(c(2,2,2,2), 'cm'),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        plot.title = element_text(size=15, hjust=0.5, face = c('bold')),
        plot.subtitle = element_text(size=10, hjust=0.5),
        axis.title = element_text(size = 15, face='bold'),
        legend.position = "none",
        axis.text.x = element_text(size=10, face='bold'),
        axis.text=element_text(color="black"))

ggsave('~/Desktop/240129.BPDCN.Freq.plot.png',
       plot=Plot)

Plot
