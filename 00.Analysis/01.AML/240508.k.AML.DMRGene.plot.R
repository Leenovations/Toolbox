library(ComplexHeatmap)
library(readxl)
library(dplyr)
#----------------------------------------------------------------------------------------------#
Onco.Data <- read_excel('/Users/lee/Desktop/AML/methylOnco.xlsx',
                        sheet = "Sheet2")
Onco.Data <- as.data.frame(Onco.Data)
Onco.Data[is.na(Onco.Data)] <- ''
rownames(Onco.Data) <- Onco.Data[,1]
Onco.Data <- Onco.Data[,-1]
#----------------------------------------------------------------------------------------------#
#color지정
col.Onco = c("CR" = "#008000",
             "NR" = "red")
#----------------------------------------------------------------------------------------------#
alter_fun = list(
  # background = alter_graphic("rect", width = 0.9, height = 0.9, fill = "#CCCCCC"),
  background = function(x, y, w, h) 
    grid.rect(x, y, w*0.9, h*0.9, gp = gpar(fill = "#CCCCCC", col = NA)),
  # CR = alter_graphic("rect", width = 0.88, height = 0.88, fill = col.Onco["CR"]),
  CR = function(x, y, w, h) 
    grid.rect(x, y, w*0.9, h*0.9, gp = gpar(fill = col.Onco["CR"], col = NA)),
  # NR = alter_graphic("rect", width = 0.88, height = 0.88, fill = col.Onco["NR"]),
  NR = function(x, y, w, h) 
    grid.rect(x, y, w*0.9, h*0.9, gp = gpar(fill = col.Onco["NR"], col = NA)),
  Promoter_Body = function(x, y, w, h) 
    grid.points(x, y, pch = '*', size = unit(.9, "char")),
  Promoter = function(x, y, w, h) 
    grid.points(x, y, pch = 16, size = unit(.65, "char")),
  Gene_Body = function(x, y, w, h) 
    grid.points(x, y, pch = 18, size = unit(.65, "char")))
#----------------------------------------------------------------------------------------------#
column_title = "CR vs NR"
#----------------------------------------------------------------------------------------------#
heatmap_legend_param = list(title = "Classification", at = c("CR", "NR", "Promoter_Body", "Promoter", "Gene_Body"), 
                            labels = c("CR hypomethylation", "NR hypomethylation", "Promoter & Gene Body", "Promoter", "Gene Body"))
#----------------------------------------------------------------------------------------------#
pdf('~/Desktop/AML.Methly.pdf', height=3, width=15)
a <- oncoPrint(Onco.Data,
               alter_fun = alter_fun, col = col.Onco, 
               column_title = NA, 
               heatmap_legend_param = heatmap_legend_param,
               row_order = rownames(Onco.Data),
               column_order = sort(colnames(Onco.Data)),
               pct_side = "NA", 
               row_names_side = "left",
               show_column_names = TRUE,
               alter_fun_is_vectorized = FALSE,
               top_annotation = NULL,
               right_annotation = NULL,
               row_names_gp = gpar(fontsize=8, fontface='bold'),
               column_names_gp = gpar(fontsize=8, fontface='italic'))
draw(a, heatmap_legend_side = "right")
dev.off()
#----------------------------------------------------------------------------------------------#
