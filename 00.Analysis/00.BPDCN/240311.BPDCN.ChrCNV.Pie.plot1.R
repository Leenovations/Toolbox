library(ggplot2)
library(dplyr) 
library(readxl)
library(patchwork)
library(viridis)
library(plotrix)
#---------------------------------------------------------------------#
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
ChrCNVPie <- ggplot(Freq.Data, aes(x = 2, y = prop, fill = Freq)) +
  geom_bar(stat = "identity", color = "white") +
  scale_fill_viridis() +
  coord_polar(theta = "y", start = 0) +
  geom_text(aes(y = lab.ypos, label = locus), color = "black", size=3) +
  theme_void() +
  xlim(1, 2.5)

ggsave('ChromosomalCNV.Pie.png',
       plot=ChrCNVPie)