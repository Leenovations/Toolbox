library(ComplexHeatmap)
getwd()
setwd('/labmed/02.AML/08.GSE163522/02.Methylkit/04.FDR/01.TF')
#------------------------------------------------------------------------------#
# TF <- read.table('/labmed/02.AML/08.GSE163522/02.Methylkit/04.FDR/01.TF/TF_Hema_Rinput.tsv',
#                  sep='\t',
#                  header = T)

TF <- read.table('/labmed/02.AML/08.GSE163522/02.Methylkit/04.FDR/01.TF/Merged_TF_RNA_Methyl.tsv',
                 sep='\t',
                 header = T)
TF_CR <- subset(TF, TF$CustomedDEG != 'None' & TF$p.value < 0.05)
TF_CR <- subset(TF_CR, (TF_CR$m.value < -0.5 & TF_CR$meth.diff > 10) | (TF_CR$m.value > 0.5 & TF_CR$meth.diff < -10))
# write.table(TF_CR$GeneSymbol, 'TF_list.tsv', sep='\t', quote = F, row.names = F, col.names = 'GeneSymbol')
#------------------------------------------------------------------------------#
TF_CR <- TF_CR[order(TF_CR$OR, decreasing = TRUE),]
#------------------------------------------------------------------------------#
Odd_CR <- TF_CR$OR
Odd_CR <- as.matrix(Odd_CR)
CR_GeneSymbol <- TF_CR$GeneSymbol
rownames(Odd_CR) <- TF_CR$GeneSymbol
#------------------------------------------------------------------------------#
col_fun = colorRamp2(c(0, max(Odd_CR)), c("white", "steelblue"))
#------------------------------------------------------------------------------#
RNA_colors <- ifelse(TF_CR$m.value > 0, "firebrick1", "forestgreen")
Meth_colors <- ifelse(TF_CR$meth.diff > 0, "forestgreen", "firebrick1")
#------------------------------------------------------------------------------#
row_right = rowAnnotation('Gene Methylation\n(beta value)\n' = anno_barplot(as.vector(TF_CR$meth.diff),
                                                                          gp = gpar(fill=Meth_colors),
                                                                          ylim=c(min(TF_CR$meth.diff), max(TF_CR$meth.diff)),
                                                                          border=F,
                                                                          bar_width = 0.8,
                                                                          axis_param=list(gp=gpar(fontsize = 8,
                                                                                                  fontface='bold'),
                                                                                          side = "top")),
                          annotation_name_gp = gpar(fontsize = 11),
                          annotation_name_side='top',
                          width=unit(4, "cm"))

row_left = rowAnnotation('Gene Expression\n(log2fc)\n' = anno_barplot(as.vector(TF_CR$m.value),
                                                                    gp = gpar(fill=RNA_colors),
                                                                    ylim=c(min(TF_CR$m.value), max(TF_CR$m.value)),
                                                                    border=F,
                                                                    bar_width = 0.8,
                                                                    axis_param = list(gp=gpar(fontsize = 8,
                                                                                              fontface='bold'),
                                                                                      # direction = "reverse",
                                                                                      side = "top")),
                         annotation_name_gp = gpar(fontsize = 11),
                         annotation_name_side='top',
                         width=unit(4, "cm"))
#------------------------------------------------------------------------------#
Plot <- Heatmap(Odd_CR,
                gap = unit(c(1.5), "mm"),
                width = unit(2, "cm"),
                height = unit(15, "cm"),
                # row_order = rownames(Odd),
                show_row_names = F,
                show_row_dend = F,
                col = col_fun,
                cluster_rows = F,
                cluster_columns = F,
                cell_fun = function(j, i, x, y, width, height, fill) {
                  grid.rect(
                    x = x, 
                    y = y, 
                    width = width * 1,  # Width of each cell
                    height = height * 1, # Height of each cell
                    gp = gpar(fill = fill, col = "black", lwd=2) # Background color
                  )
                  grid.text(
                    sprintf("%s", CR_GeneSymbol[i]), 
                    x = x, 
                    y = y, 
                    gp = gpar(fontsize = 10)
                  )
                },
                row_title_gp = gpar(fontsize=0),
                show_heatmap_legend = F,
                right_annotation=row_right,
                left_annotation=row_left)
#------------------------------------------------------------------------------#
lgd1 = Legend(col_fun = col_fun,
              title = "odd ratio\n(TF binding)\n",
              direction = "vertical",
              at = c(0, max(Odd_CR)),
              labels = c("low", "high"),
              border = "black",
              title_gp = gpar(fontsize = 15),
              labels_gp = gpar(fontsize = 13),
              legend_height = unit(3, "cm"),
              grid_width = unit(0.5, "cm"),
              title_position = "leftcenter-rot")

lgd2 = Legend(labels = c('CR Hypomethylation & Up regulation', 'NR Hypomethylation & Up regulation'), 
              title = '',
              labels_gp = gpar(fontsize = 13),
              legend_gp = gpar(fill = c('forestgreen', 'firebrick1')),
              title_position = "lefttop")

lgd = packLegend(lgd1, lgd2, direction = "vertical")
#------------------------------------------------------------------------------#
pdf('Figure3B-1.pdf', height=10, width=8)
draw(Plot, 
     heatmap_legend_side='bottom',
     row_split = rep(c(seq(1, nrow(Odd_CR))), 1))
draw(lgd, x = unit(5, "cm"), y = unit(3, "cm"))
dev.off()
#------------------------------------------------------------------------------#
