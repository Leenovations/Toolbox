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

Onco.Data <- read_excel('/Users/lee/Documents/03.NGS/05.GS/01.BPDCN/02.Table/240122.Oncotable.final.xlsx', sheet = 'Exclude')
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
                       sheet = 'Enrichment')
Function <- as.data.frame(Function)
Function <- Function[grepl('Summary', Function[,1]),]

Hemopoiesis <- Function[3,8]
Hemopoiesis <- unlist(strsplit(Hemopoiesis, ','))

Cancer <- Function[2, 8]
Cancer <- unlist(strsplit(Cancer, ','))
Cancer <- setdiff(Cancer, Hemopoiesis)

Chromatin <- Function[7, 8]
Chromatin <- unlist(strsplit(Chromatin, ','))
Chromatin <- Reduce(setdiff, list(Chromatin, Hemopoiesis, Cancer))

lymphocyte <- Function[16, 8]
lymphocyte <- unlist(strsplit(lymphocyte, ','))
lymphocyte <- Reduce(setdiff, list(lymphocyte, Chromatin, Hemopoiesis, Cancer))

Gene <- rownames(Onco.Data)

Hemopoiesis <- Onco.Data %>%
  filter(Gene %in% Hemopoiesis)
# rownames(Hemopoiesis) <- Hemopoiesis
# Hemopoiesis <- Hemopoiesis[-1]

Cancer <- Onco.Data %>%
  filter(Gene %in% Cancer)
# rownames(Cancer) <- Cancer$Gene
# Cancer <- Cancer[-1]

Chromatin <- Onco.Data %>%
  filter(Gene %in% Chromatin)
# rownames(Chromatin) <- Chromatin$Gene
# Chromatin <- Chromatin[-1]

lymphocyte <- Onco.Data %>%
  filter(Gene %in% lymphocyte)
# rownames(lymphocyte) <- lymphocyte$Gene
# lymphocyte <- lymphocyte[-1]

Onco.func.Data <- rbind(Hemopoiesis, Cancer, Chromatin, lymphocyte)
nrow(Onco.func.Data)
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
     row_split = rep(c('Hematopoiesis', 'Cancer pathway', 'Chromatin organization', 'Lymphocyte\nRegulation'),c(33,20,13,10)))
dev.off()
