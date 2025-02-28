library(ggplot2)
library(dplyr) 
library(readxl)
library(patchwork)
library(viridis)
library(plotrix)
#---------------------------------------------------------------------#
setwd('/labmed/06.BPDCN/')
Freq.Data <- read.table('BPDCN.ChromosomalCNV.CHR.Freq.input.txt', sep='\t', header = T)
Freq.Data <- subset(Freq.Data, Freq.Data$Freq > 0)
Freq.Data$prop <- Freq.Data$Freq / sum(Freq.Data$Freq) * 100
#---------------------------------------------------------------------#
idx_order <- order(Freq.Data$prop, decreasing = TRUE)
Freq.Data <- Freq.Data[idx_order, ]
#---------------------------------------------------------------------#
Freq.Data <- Freq.Data %>%
  arrange(desc(Freq)) %>%
  mutate(lab.ypos = cumsum(prop) - 0.5*prop)
#---------------------------------------------------------------------#
data <- Freq.Data$prop

pdf('ChrCNVPie.pdf', width=7)
Plot <- pie3D(data,
      col = hcl.colors(length(data), "Spectral"),
      labels = Freq.Data$locus,
      theta=pi/3,
      height=0.1,
      labelcex=1.3,
      explode=0.1,
      main='Chromosomal Copy Number Frequency')
dev.off()

png('ChrCNVPie.png', width=600,height=500,unit="px")
Plot <- pie3D(data,
              col = hcl.colors(length(data), "Spectral"),
              labels = Freq.Data$locus,
              theta=pi/3,
              height=0.1,
              labelcex=1.3,
              explode=0.1,
              main='Chromosomal Copy Number Frequency')
dev.off()
