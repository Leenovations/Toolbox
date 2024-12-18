library(ggplot2)

args <- commandArgs(trailingOnly = TRUE)
Group_A <- args[1]
Group_B <- args[2]
#------------------------------------------------------------------------#
current_date <- Sys.Date()
Date <- format(current_date, "%y%m%d")
#------------------------------------------------------------------------#
Data <- read.table('Result/00.Tables/230825.Methyl.2kb.Group.txt', sep='\t', header=T)
Data <- Data[complete.cases(Data),]
#------------------------------------------------------------------------#
pdf(paste0('Result/01.Plots/', 'Density.plot.pdf'))

ggplot(Data, aes(x = !!sym(Group_A), y = !!sym(Group_B))) +
  geom_density_2d() +
  geom_density_2d_filled() +
  labs(x=Group_A, y=Group_B, title='Group specific CpG Methylation Distribution') +
  theme_test() + 
  coord_fixed(ratio = 1:1) +
  scale_x_continuous(breaks = c(0, 25, 50, 75, 100), expand = c(0, 0)) +
  scale_y_continuous(breaks = c(0, 25, 50, 75, 100), expand = c(0, 0)) +
  theme(legend.position = 'none',
        plot.title=element_text(hjust=0.5))

dev.off()