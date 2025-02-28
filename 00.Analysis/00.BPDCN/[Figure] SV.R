library(ComplexHeatmap)
library(circlize)
#------------------------------------------------------------------------------#
pdf('/labmed/00.Code/ToolBox/00.Analysis/00.BPDCN/Circos/00.Translocation/BPDCN.translocation.pdf',
    width=11, height=11)
#------------------------------------------------------------------------------#
Donor_four <- read.table('/labmed/00.Code/ToolBox/00.Analysis/00.BPDCN/Circos/00.Translocation/BPDCN.chr.link.donor.sorted.4.bed',
                         sep='\t',
                         col.names=c('chr','start','end', 'gene'))
Acceptor_four <- read.table('/labmed/00.Code/ToolBox/00.Analysis/00.BPDCN/Circos/00.Translocation/BPDCN.chr.link.acceptor.sorted.4.bed',
                            sep='\t',
                            col.names=c('chr','start','end', 'gene'))
#------------------------------------------------------------------------------#
Donor_three <- read.table('/labmed/00.Code/ToolBox/00.Analysis/00.BPDCN/Circos/00.Translocation/BPDCN.chr.link.donor.sorted.3.bed',
                          sep='\t',
                          col.names=c('chr','start','end', 'gene'))
Acceptor_three <- read.table('/labmed/00.Code/ToolBox/00.Analysis/00.BPDCN/Circos/00.Translocation/BPDCN.chr.link.acceptor.sorted.3.bed',
                             sep='\t',
                             col.names=c('chr','start','end', 'gene'))
#------------------------------------------------------------------------------#
Donor_two <- read.table('/labmed/00.Code/ToolBox/00.Analysis/00.BPDCN/Circos/00.Translocation/BPDCN.chr.link.donor.sorted.2.bed',
                        sep='\t',
                        col.names=c('chr','start','end', 'gene'))
Acceptor_two <- read.table('/labmed/00.Code/ToolBox/00.Analysis/00.BPDCN/Circos/00.Translocation/BPDCN.chr.link.acceptor.sorted.2.bed',
                           sep='\t',
                           col.names=c('chr','start','end', 'gene'))
#------------------------------------------------------------------------------#
Donor_one <- read.table('/labmed/00.Code/ToolBox/00.Analysis/00.BPDCN/Circos/00.Translocation/BPDCN.chr.link.donor.sorted.1.bed',
                        sep='\t',
                        col.names=c('chr','start','end', 'gene'))
Acceptor_one <- read.table('/labmed/00.Code/ToolBox/00.Analysis/00.BPDCN/Circos/00.Translocation/BPDCN.chr.link.acceptor.sorted.1.bed',
                           sep='\t',
                           col.names=c('chr','start','end', 'gene'))
#------------------------------------------------------------------------------#
cytoband = read.cytoband()$df
circos.genomicInitialize(cytoband, plotType = NULL)
#------------------------------------------------------------------------------#
Total_label <- unique(read.table('/labmed/00.Code/ToolBox/00.Analysis/00.BPDCN/Circos/00.Translocation/BPDCN.chr.gene.bed',
                                 sep='\t', col.names=c('chr', 'start', 'end', 'gene')))
circos.genomicLabels(Total_label, 
                     labels.column = 4, 
                     side = "outside", 
                     cex=1, 
                     connection_height = mm_h(3),
                     line_lty = 'solid')
#------------------------------------------------------------------------------#
circos.genomicIdeogram(cytoband)
circos.par(track.margin = c(0.01, 0.03)) 
circos.track(track.index = get.current.track.index(), panel.fun = function(x, y) {
  circos.text(CELL_META$xcenter, CELL_META$ylim[1], CELL_META$sector.index,
              niceFacing = TRUE, adj = c(0.5, 1.5), cex = 0.8)
}, track.height = strheight("fj", cex = 0.8)*1.2, bg.border = NA, cell.padding = c(0, 0, 0, 0))
#------------------------------------------------------------------------------#
circos.genomicLink(Donor_four, Acceptor_four,  
                   col='coral', 
                   lwd=8)
circos.genomicLink(Donor_three, Acceptor_three,  
                   col='coral', 
                   lwd=5)
circos.genomicLink(Donor_two, Acceptor_two,  
                   col='coral', 
                   lwd=3)
circos.genomicLink(Donor_one, Acceptor_one,  
                   col='coral', 
                   lwd=1)
#------------------------------------------------------------------------------#
lgd_lines = Legend(at = c("Translocation"),
                   type = "lines", 
                   legend_gp = gpar(col = c('coral'), 
                                    lwd = 2,
                                    fontsize = 15), 
                   title = "Type",
                   labels_gp = gpar(fontsize = 13))
draw(lgd_lines, just = c(-2.5,13))
#------------------------------------------------------------------------------#
dev.off()
