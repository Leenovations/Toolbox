library(ComplexHeatmap)
library(readxl)
library(dplyr)

Annotation <- read.table('/Users/lee/Documents/03.NGS/05.GS/01.BPDCN/02.Table/230825.BPDCN.Involve.Site.txt', 
                         sep = '\t',
                         header=T,
                         row.names = 1)
Annotation <- Annotation[c('BPDCN10', 'BPDCN6', 'BPDCN1', 'BPDCN2', 'BPDCN7', 'BPDCN8', 'BPDCN13', 'BPDCN11', 'BPDCN12', 'BPDCN3', 'BPDCN5', 'BPDCN9', 'BPDCN4'),]

ha = HeatmapAnnotation(Sex = Annotation$Sex,
                       Age = Annotation$Age,
                       "Involvement site" = Annotation$Involvement,
                       "Induction chemotherapy"=Annotation$Induction,
                       "L-asparaginase"=Annotation$Contating,
                       Transplantation=Annotation$Transplantation,
                       Cytogenetics=Annotation$Cytogenetics,
                       Survival=Annotation$Survival,
                       col = list(Sex = c('Male'='#0070C0', 'Female'='firebrick3'),
                                  Age = c('≥55 years'='#FF66CC', '<55 years'='#9900FF'),
                                  "Involvement site" = c("Multiple skin ± systemic" = "#31869B",
                                                         "Systemic without skin" = "#76933C",
                                                         "Single skin" = "#E26B0A"),
                                  "Induction chemotherapy" = c('AML-like chemotherapy'='#95B3D7', 
                                                'ALL-like chemotherapy'='#DA9694', 
                                                'Lymphoma-like chemotherapy'='#B1A0C7'),
                                  "L-asparaginase" = c('Yes'='#244062', 
                                                       'No'='#DCE6F1'),
                                  Transplantation = c('Allo-SCT'='#9966FF', 
                                                      'Salvage auto-SCT'='#00CC00', 
                                                      'Salvage Allo-SCT'='#9966FF',
                                                      'None'='gray80'),
                                  Cytogenetics = c('Abnormal'='#993300', 
                                                   'Normal'='#CC6633', 
                                                   'Not available'='gray80'),
                                  Survival = c('<18 months'='#00B0F0', 
                                               '≥18 months'='#FFC000')),
                       annotation_height = unit(c(5, 5, 100), "mm"),
                       annotation_name_gp = gpar(fontsize = 8),
                       annotation_name_side = 'left')

Onco.Data <- read_excel('/Users/lee/Documents/03.NGS/05.GS/01.BPDCN/02.Table/[BPDCN] Variation.exclude.non.Info.xlsx', sheet = 'Oncotable')
Onco.Data <- as.data.frame(Onco.Data)
Onco.Data <- Onco.Data[order(-rowSums(!is.na(Onco.Data))), ]
Onco.Data[is.na(Onco.Data)] <- ''
rownames(Onco.Data) <- Onco.Data[,1]
Onco.Data <- Onco.Data[,-1]
colnames(Onco.Data)

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
                            labels = c("Missense", "Truncating", "Duplication", "Deletion", "Copy number Amplification","Copy number Deletion"))

Onco.func.Data <- Onco.Data[,c('BPDCN10', 'BPDCN6', 'BPDCN1', 'BPDCN2', 'BPDCN7', 'BPDCN8', 'BPDCN13', 'BPDCN11', 'BPDCN12', 'BPDCN3', 'BPDCN5', 'BPDCN9', 'BPDCN4')]
colnames(Onco.func.Data) <- c('8','2', '16', '17', '3', '5', '30', '9', '12', '39', '29', '7', '18')
pdf('~/Desktop/[BPDCN] Oncoprint.pdf', height=15, width=9)
a <- oncoPrint(Onco.func.Data,
               alter_fun = alter_fun, col = col.Onco,
               gap = unit(c(1.5), "mm"),
               column_title = column_title, heatmap_legend_param = heatmap_legend_param,
               pct_side = "right", row_names_side = "left",
               alter_fun_is_vectorized = FALSE,
               bottom_annotation = ha,
               column_names_rot = 0,
               column_order = colnames(Onco.func.Data),
               # show_column_names = TRUE,
               row_names_gp = gpar(fontsize=8, fontface='italic'),
               pct_gp = gpar(fontsize=8),
               row_title_gp = gpar(fontsize=10, fontface='bold'))
draw(a, heatmap_legend_side = "right", 
     annotation_legend_side = "bottom", 
     merge_legend = TRUE)
dev.off()
#-------------------------------------------------------------------------------------------#
library(ComplexHeatmap)
library(readxl)
library(dplyr)
library(grid)

Annotation <- read.table('/Users/lee/Documents/03.NGS/05.GS/01.BPDCN/02.Table/230825.BPDCN.Involve.Site.txt', 
                         sep = '\t',
                         header=T,
                         row.names = 1)

Annotation <- Annotation %>%
  select(-Induction, -Contating, -Transplantation)

Annotation <- Annotation[c('BPDCN10', 'BPDCN6', 'BPDCN1', 'BPDCN2', 'BPDCN7', 'BPDCN8', 'BPDCN13', 'BPDCN11', 'BPDCN12', 'BPDCN3', 'BPDCN5', 'BPDCN9', 'BPDCN4'),]

ha = HeatmapAnnotation(Sex = Annotation$Sex,
                       Age = Annotation$Age,
                       "Involvement site" = Annotation$Involvement,
                       Cytogenetics=Annotation$Cytogenetics,
                       Survival=Annotation$Survival,
                       col = list(Sex = c('Male'='#0070C0', 'Female'='firebrick3'),
                                  Age = c('≥55 years'='#FF66CC', '<55 years'='#9900FF'),
                                  "Involvement site" = c("Multiple skin ± systemic" = "#31869B",
                                                         "Systemic without skin" = "#76933C",
                                                         "Single skin" = "#E26B0A"),
                                  Cytogenetics = c('Abnormal'='#993300', 
                                                   'Normal'='#CC6633', 
                                                   'Not available'='gray80'),
                                  Survival = c('<18 months'='#00B0F0', 
                                               '≥18 months'='#FFC000')),
                       annotation_height = unit(c(5, 5, 100), "mm"),
                       annotation_name_gp = gpar(fontsize = 8),
                       annotation_name_side = 'left')

Onco.Data <- read_excel('/Users/lee/Documents/03.NGS/05.GS/01.BPDCN/02.Table/[BPDCN] Variation.exclude.non.Info.xlsx', sheet = 'Oncotable')
Onco.Data <- as.data.frame(Onco.Data)
Onco.Data <- Onco.Data[order(-rowSums(!is.na(Onco.Data))), ]
Onco.Data[is.na(Onco.Data)] <- ''
rownames(Onco.Data) <- Onco.Data[,1]
Onco.Data <- Onco.Data[,-1]
colnames(Onco.Data)

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
  Truncating = alter_graphic("rect", fill = col.Onco["Truncating"]),
  Duplication = alter_graphic("rect", height = 0.23, fill = col.Onco["Duplication"]),
  Deletion = alter_graphic("rect", height = 0.23, fill = col.Onco["Deletion"]),
  Copy_number_Amplification = alter_graphic("rect", height = 0.23, fill = col.Onco["Copy_number_Amplification"]),
  Copy_number_Deletion = alter_graphic("rect", height = 0.23, fill = col.Onco["Copy_number_Deletion"])
)

column_title = "Altered in 13 of 13 BPDCN samples"
heatmap_legend_param = list(title = "Alternations", at = c("Missense", "Truncating", "Duplication", "Deletion", "Copy_number_Amplification","Copy_number_Deletion"), 
                            labels = c("Missense", "Truncating", "Insertion", "Deletion", "Copy number amplification","Copy number deletion"))

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
Onco.func.Data <- Onco.func.Data[,c('BPDCN10', 'BPDCN6', 'BPDCN1', 'BPDCN2', 'BPDCN7', 'BPDCN8', 'BPDCN13', 'BPDCN11', 'BPDCN12', 'BPDCN3', 'BPDCN5', 'BPDCN9', 'BPDCN4')]
colnames(Onco.func.Data) <- c('8','2', '16', '17', '3', '5', '30', '9', '12', '39', '29', '7', '18')
pdf('~/Desktop/Legend.pdf', height=15, width=9)
a <- oncoPrint(Onco.func.Data,
               alter_fun = alter_fun, col = col.Onco,
               gap = unit(c(1.5), "mm"),
               column_title = column_title, heatmap_legend_param = heatmap_legend_param,
               pct_side = "right", row_names_side = "left",
               alter_fun_is_vectorized = FALSE,
               bottom_annotation = ha,
               column_names_rot = 0,
               column_names_centered = TRUE,
               name = 'UPN',
               column_order = colnames(Onco.func.Data),
               show_column_names = TRUE,
               row_names_gp = gpar(fontsize=8, fontface='italic'),
               pct_gp = gpar(fontsize=8),
               row_title_gp = gpar(fontsize=10, fontface='bold'))
draw(a, heatmap_legend_side = "right", 
     annotation_legend_side = "bottom", 
     merge_legend = TRUE, 
     row_split = rep(c('Chromatin remodeling', 'Protein kinase pathway', 'Cell cycle', 'Methylation', 'Cell\ndifferentiation', 'RAS signaling'),
                     c(nrow(chromatin_remodeling),nrow(Protein_kinase),nrow(Cell_Cycle),nrow(Methylation), nrow(Cell_differentiation), nrow(RAS))))
grid.text("UPN", x = 0.0899, y = 0.011, gp = gpar(fontsize = 8, col = "black"))
dev.off()
