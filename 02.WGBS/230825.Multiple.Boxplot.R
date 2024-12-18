library(ggplot2)

Data <- read.table('Result/00.Tables/Multiple_Boxplot.txt',
                   header=T,
                   sep='\t')

Plot <- ggplot(Data, aes(x=Type, y=Meth, color=Group)) +
  geom_boxplot() +
  scale_color_manual(values = c('CR'='tan1', 'NR'='lightskyblue')) +
  theme_test() +
  labs(title='Mean Methylation of specific region',
       x='',
       y='Methylation Level (%)') +
  theme(plot.title = element_text(hjust=0.5),
        legend.position='top')

ggsave(file='Result/01.Plots/Multiple_boxplot.pdf')
