library(ggplot2)
library(readxl)
#------------------------------------------------------------------------------#
TPM <- read_excel('/labmed/01.AML/240123.AML.Total.Info.xlsx', sheet='RNA_TPM')
GeneSet <- paste0('/labmed/01.AML/03.Common/00.GeneSet/', list.files('/labmed/01.AML/03.Common/00.GeneSet/', '*'))
#------------------------------------------------------------------------------#
for (geneset in GeneSet) {
  Pathway_name <- gsub('/labmed/01.AML/03.Common/00.GeneSet/', '', geneset)
  Pathway_name <- strsplit(Pathway_name, '\\.')[[1]]
  Pathway_name <- Pathway_name[1]
  Pathway_title <- gsub('_', ' ', Pathway_name)
  Pathway <- read.table(geneset, sep='\t', header=T)
  for (gene in Pathway$Gene) {
    TPM_Sub <- subset(TPM, TPM$GeneSymbol == gene)
    if (dim(TPM_Sub)[1] == 1) {
      TPM_Sub <- as.data.frame(TPM_Sub)
      TPM_Sub <- TPM_Sub[, -1]
      rownames(TPM_Sub) <- TPM_Sub[1]
      TPM_Sub <- TPM_Sub[, -1]
      TPM_Sub <-t(TPM_Sub)
      TPM_Sub <- as.data.frame(TPM_Sub)
      colnames(TPM_Sub) <- 'TPM'
      TPM_Sub$Sample <- rownames(TPM_Sub)
      TPM_Sub$Group <- rep(c('CR', 'NR'), c(8,5))

      Plot <- ggplot(TPM_Sub, aes(x=Sample, y=TPM, fill=Group, color=Group)) +
              geom_bar(stat = "identity",
                       position = "identity") +
              scale_fill_manual(values=c('tan1', 'lightskyblue')) +
              scale_color_manual(values=c('black', 'black')) +
              theme_classic() +
              xlab('') +
              ylab('TPM') +
              scale_y_continuous(expand = c(0,0)) +
              ggtitle(gene, subtitle = paste0('\n','(',Pathway_title, ')', '\n')) +
              theme(plot.margin = unit(c(2,2,2,2), 'cm'),
                    panel.grid.major = element_blank(),
                    panel.grid.minor = element_blank(),
                    axis.title.y = element_text(size=10, face='bold'),
                    plot.title = element_text(size=15, hjust=0.5, face = c('bold.italic')),
                    plot.subtitle = element_text(size=10, hjust=0.5),
                    axis.title = element_text(size = 10),
                    legend.position = "none",
                    axis.text=element_text(color="black"))

      ggsave(paste0('/labmed/01.AML/04.Results/00.Plot/', Pathway_name, '.', gene, '.png'),
             plot=Plot)
    }
  }
}
