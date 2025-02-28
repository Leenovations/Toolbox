library(ComplexHeatmap)
library(readxl)
library(dplyr)

Annotation <- read.table('/Users/lee/Documents/03.NGS/05.GS/01.BPDCN/02.Table/230825.BPDCN.Involve.Site.txt', 
                         sep = '\t',
                         header=T,
                         row.names = 1)

ha = HeatmapAnnotation("Involvement site" = Annotation$Involvement,
                       Age = Annotation$Age,
                       Sex = Annotation$Sex,
                       Induction=Annotation$Induction,
                       Cytogenetics=Annotation$Cytogenetics,
                       "L-asparaginase"=Annotation$Contating,
                       Transplantation=Annotation$Transplantation,
                       Survival=Annotation$Survival,
                       col = list("Involvement site" = c("Multiple skin ± systemic" = "springgreen4",
                                                         "Systemic without skin" = "springgreen3",
                                                         "Single skin" = "springgreen1"),
                                  Age = c('>=60 years'='gold', '<60 years'='lightgoldenrod1'),
                                  Cytogenetics = c('Abnormal'='#993300', 'Normal'='#CC6633', 'Not available'='gray80'),
                                  Sex = c('Male'='steelblue1', 'Female'='skyblue1'),
                                  Induction = c('AML-like chemotherapy'='slateblue4', 'ALL-like chemotherapy'='slateblue3', 'Lymphoma-like chemotherapy'='mediumpurple1'),
                                  "L-asparaginase" = c('Yes'='royalblue4', 'No'='gray80'),
                                  Transplantation = c('Allo-SCT'='indianred3', 'Salvage auto-SCT'='lightpink', 'Salvage Allo-SCT'='hotpink1','None'='gray80'),
                                  Survival = c('<24 months'='violetred1', '>=24 months'='plum2')),
                       annotation_height = unit(c(5, 5, 100), "mm"),
                       annotation_name_gp= gpar(fontsize = 8))

Onco.Data <- read_excel('/Users/lee/Documents/03.NGS/05.GS/01.BPDCN/02.Table/240122.Oncotable.final.xlsx',
                        sheet = "Exclude")
Onco.Data <- as.data.frame(Onco.Data)
Onco.Data <- Onco.Data[order(-rowSums(!is.na(Onco.Data))), ]
Onco.Data[is.na(Onco.Data)] <- ''
rownames(Onco.Data) <- Onco.Data[,1]
Onco.Data <- Onco.Data[,-1]
Onco.Data <- Onco.Data[1:50,]

#color지정
col.Onco = c("Missense" = "#008000", 
             "Truncating" = "red", 
             "Duplication" = "blue", 
             "Deletion" = "orange",
             "Copy_number_Amplification" = "purple",
             "Copy_number_Deletion" = "navy")

alter_fun = list(
  background = alter_graphic("rect", fill = "#CCCCCC"),
  Missense = alter_graphic("rect", fill = col.Onco["Missense"]),
  Truncating = alter_graphic("rect", height = 0.23, fill = col.Onco["Truncating"]),
  Duplication = alter_graphic("rect", height = 0.23, fill = col.Onco["Duplication"]),
  Deletion = alter_graphic("rect", height = 0.23, fill = col.Onco["Deletion"]),
  Copy_number_Amplification = alter_graphic("rect", height = 0.23, fill = col.Onco["Copy_number_Amplification"]),
  Copy_number_Deletion = alter_graphic("rect", height = 0.23, fill = col.Onco["Copy_number_Deletion"])
)

column_title = "Altered in 13 of 13 BPDCN samples"
heatmap_legend_param = list(title = "Alternations", at = c("Missense", "Truncating", "Duplication", "Deletion", "Copy_number_Amplification","Copy_number_Deletion"), 
                            labels = c("Missense", "Truncating", "Duplication", "Deletion", "Copy_number_Amplification","Copy_number_Deletion"))

pdf('~/Desktop/240312.BPDCN.Oncoprint.pdf', height=15)
a <- oncoPrint(Onco.Data,
               alter_fun = alter_fun, col = col.Onco, 
               column_title = column_title, heatmap_legend_param = heatmap_legend_param,
               pct_side = "right", row_names_side = "left",
               alter_fun_is_vectorized = FALSE,
               bottom_annotation = ha,
               column_order = colnames(Onco.Data),
               row_names_gp = gpar(fontsize=7, fontface='italic'),
               pct_gp = gpar(fontsize=7),
               row_title_gp = gpar(fontsize=4))
draw(a, heatmap_legend_side = "bottom", annotation_legend_side = "bottom", merge_legend = TRUE,
     row_gap = unit(100, "mm"))
dev.off()


#------------------------------------------------------------------------------#
library(ComplexHeatmap)
library(readxl)
library(dplyr)

Annotation <- read.table('/Users/lee/Documents/03.NGS/05.GS/01.BPDCN/02.Table/230825.BPDCN.Involve.Site.txt', 
                         sep = '\t',
                         header=T,
                         row.names = 1)

ha = HeatmapAnnotation("Involvement site" = Annotation$Involvement,
                       Age = Annotation$Age,
                       Sex = Annotation$Sex,
                       Induction=Annotation$Induction,
                       Cytogenetics=Annotation$Cytogenetics,
                       "L-asparaginase"=Annotation$Contating,
                       Transplantation=Annotation$Transplantation,
                       Survival=Annotation$Survival,
                       col = list("Involvement site" = c("Multiple skin ± systemic" = "springgreen4",
                                                         "Systemic without skin" = "springgreen3",
                                                         "Single skin" = "springgreen1"),
                                  Age = c('>=60 years'='gold', '<60 years'='lightgoldenrod1'),
                                  Cytogenetics = c('Abnormal'='#993300', 'Normal'='#CC6633', 'Not available'='gray80'),
                                  Sex = c('Male'='steelblue1', 'Female'='skyblue1'),
                                  Induction = c('AML-like chemotherapy'='slateblue4', 'ALL-like chemotherapy'='slateblue3', 'Lymphoma-like chemotherapy'='mediumpurple1'),
                                  "L-asparaginase" = c('Yes'='royalblue4', 'No'='gray80'),
                                  Transplantation = c('Allo-SCT'='indianred3', 'Salvage auto-SCT'='lightpink', 'Salvage Allo-SCT'='hotpink1','None'='gray80'),
                                  Survival = c('<24 months'='violetred1', '>=24 months'='plum2')),
                       annotation_height = unit(c(5, 5, 100), "mm"),
                       annotation_name_gp= gpar(fontsize = 8))

Onco.Data <- read_excel('/Users/lee/Documents/03.NGS/05.GS/01.BPDCN/02.Table/[BPDCN] Variation.exclude.non.Info.xlsx', sheet = 'Oncotable')
Onco.Data <- as.data.frame(Onco.Data)
Onco.Data <- Onco.Data[order(-rowSums(!is.na(Onco.Data))), ]
Onco.Data[is.na(Onco.Data)] <- ''
rownames(Onco.Data) <- Onco.Data[,1]
Onco.Data <- Onco.Data[,-1]

#color지정
col.Onco = c("Missense" = "#008000", 
             "Truncating" = "red", 
             "Duplication" = "blue", 
             "Deletion" = "orange",
             "Copy_number_Amplification" = "purple",
             "Copy_number_Deletion" = "navy")

alter_fun = list(
  background = alter_graphic("rect", fill = "#CCCCCC"),
  Missense = alter_graphic("rect", fill = col.Onco["Missense"]),
  Truncating = alter_graphic("rect", height = 0.23, fill = col.Onco["Truncating"]),
  Duplication = alter_graphic("rect", height = 0.23, fill = col.Onco["Duplication"]),
  Deletion = alter_graphic("rect", height = 0.23, fill = col.Onco["Deletion"]),
  Copy_number_Amplification = alter_graphic("rect", height = 0.23, fill = col.Onco["Copy_number_Amplification"]),
  Copy_number_Deletion = alter_graphic("rect", height = 0.23, fill = col.Onco["Copy_number_Deletion"])
)

column_title = "Altered in 13 of 13 BPDCN samples"
heatmap_legend_param = list(title = "Alternations", at = c("Missense", "Truncating", "Duplication", "Deletion", "Copy_number_Amplification","Copy_number_Deletion"), 
                            labels = c("Missense", "Truncating", "Duplication", "Deletion", "Copy_number_Amplification","Copy_number_Deletion"))


Function <- read_excel('/Users/lee/Documents/03.NGS/05.GS/01.BPDCN/02.Table/240129.BPDCN.metascape.xlsx',
                       sheet = 'Oncoplot')
Function <- as.data.frame(Function)

Methylation <- Function[8, 8]
Methylation <- unlist(strsplit(Methylation, ','))

chromatin_remodeling <- Function[1,8]
chromatin_remodeling <- unlist(strsplit(chromatin_remodeling, ','))
chromatin_remodeling <- Reduce(setdiff, list(chromatin_remodeling,Methylation))

Protein_kinase <- Function[2, 8]
Protein_kinase <- unlist(strsplit(Protein_kinase, ','))
Protein_kinase <- Reduce(setdiff, list(Protein_kinase, chromatin_remodeling, Methylation))

Cell_Cycle <- Function[3, 8]
Cell_Cycle <- unlist(strsplit(Cell_Cycle, ','))
Cell_Cycle <- Reduce(setdiff, list(Cell_Cycle, chromatin_remodeling, Protein_kinase, Methylation))

Cell_differentiation <- Function[5, 8]
Cell_differentiation <- unlist(strsplit(Cell_differentiation, ','))
Cell_differentiation <- Reduce(setdiff, list(Cell_differentiation, Methylation, Cell_Cycle, chromatin_remodeling, Protein_kinase))

RAS <- Function[6, 8]
RAS <- unlist(strsplit(RAS, ','))
RAS <- Reduce(setdiff, list(RAS, Methylation, Cell_Cycle, chromatin_remodeling, Protein_kinase, Cell_differentiation))

Gene <- rownames(Onco.Data)

chromatin_remodeling <- Onco.Data %>%
  filter(Gene %in% chromatin_remodeling)

Protein_kinase <- Onco.Data %>%
  filter(Gene %in% Protein_kinase)

Cell_Cycle <- Onco.Data %>%
  filter(Gene %in% Cell_Cycle)

Methylation <- Onco.Data %>%
  filter(Gene %in% Methylation)

Cell_differentiation <- Onco.Data %>%
  filter(Gene %in% Cell_differentiation)

RAS <- Onco.Data %>%
  filter(Gene %in% RAS)

Onco.func.Data <- rbind(chromatin_remodeling, Protein_kinase, Cell_Cycle, Methylation, Cell_differentiation, RAS)
pdf('~/Desktop/240312.BPDCN.Oncoprint.function.pdf', height=15)
a <- oncoPrint(Onco.func.Data,
               alter_fun = alter_fun, col = col.Onco,
               gap = unit(c(1.5), "mm"),
               column_title = column_title, heatmap_legend_param = heatmap_legend_param,
               pct_side = "right", row_names_side = "left",
               alter_fun_is_vectorized = FALSE,
               bottom_annotation = ha,
               column_order = colnames(Onco.Data),
               row_names_gp = gpar(fontsize=6, fontface='italic'),
               pct_gp = gpar(fontsize=4),
               row_title_gp = gpar(fontsize=9))
draw(a, heatmap_legend_side = "bottom", annotation_legend_side = "bottom", merge_legend = TRUE,
     row_split = rep(c('Chromatin remodeling', 'Protein kinase pathway', 'Cell cycle', 'Methylation', 'Cell\ndifferentiation', 'RAS signaling'),
                     c(nrow(chromatin_remodeling),nrow(Protein_kinase),nrow(Cell_Cycle),nrow(Methylation), nrow(Cell_differentiation), nrow(RAS))))
dev.off()
