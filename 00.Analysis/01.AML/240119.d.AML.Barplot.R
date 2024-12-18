library(readxl)
library(ggpubr)

Data <- read_excel('/labmed/11.AML/230625.AML.Total.Data.xlsx', sheet='Norm.Over.50')

Gene <- c('TAL1', 'BCL11A', 'GATA1', 'GATA2', 'NFE2')
for (gene in Gene){
    Sub_Data <- subset(Data, Data$Gene == gene)
    Sub_Data <- Sub_Data[-1]
    Trans_Data <- t(Sub_Data)
    Trans_Data <- as.data.frame(Trans_Data)
    colnames(Trans_Data) <- c('NormConunt')
    Trans_Data$Group <- rep(c('CR', 'NR'), c(8, 5))

    bp <- ggboxplot(Trans_Data, x = "Group", y = "NormConunt", fill = "Group", 
                palette = c("tan1", "lightskyblue"))

     ggsave(paste0('/labmed/11.AML/', gene, '.barplot.png'),
        width = 5,
        height=5,
        plot=bp)
}