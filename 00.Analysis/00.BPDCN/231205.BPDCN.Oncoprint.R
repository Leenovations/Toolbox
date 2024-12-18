library(ComplexHeatmap)
library(readxl)
library(dplyr)

Annotation <- read.table('/Users/lee/Documents/05.대학원/01.BPDCN/03.Table/230825.BPDCN.Involve.Site.txt', 
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

Onco.Data <- read_excel('~/Desktop/231205.BPDCN.Oncoprint.xlsx',
                        sheet='OncoPrint')
Onco.Data <- as.data.frame(Onco.Data)
# Onco.Data <- Onco.Data[order(-rowSums(!is.na(Onco.Data))), ]
Onco.Data[is.na(Onco.Data)] <- ''
rownames(Onco.Data) <- Onco.Data[,1]
Onco.Data <- Onco.Data[,-1]
Onco.Data <- Onco.Data[,c(4,3,5,9,12,11,10,8,7,1,2,6,13)]

#color지정
col.Onco = c("Missense" = "#008000", "Truncating" = "red", "Splicing" = "orange", "Amplification" = "blue", "Deletion" = "navy")

alter_fun = list(
  background = function(x, y, w, h) {
    grid.rect(x, y, w-unit(0.948, "pt"), h-unit(0.948, "pt"), 
              gp = gpar(fill = "#CCCCCC", col = NA))
  },
  # big green
  Missense = function(x, y, w, h) {
    grid.rect(x, y, w-unit(0.948, "pt"), h-unit(0.948, "pt"), 
              gp = gpar(fill = col["Missense"], col = NA))
  },
  # big red
  Truncating = function(x, y, w, h) {
    grid.rect(x, y, w-unit(0.93, "pt"), h*0.33, 
              gp = gpar(fill = col["Truncating"], col = NA))
  },
  # big orange
  Splicing = function(x, y, w, h) {
    grid.rect(x, y, w-unit(0.948, "pt"), h-unit(0.948, "pt"), 
              gp = gpar(fill = col["Splicing"], col = NA))
  },
  # big navy
  Amplification = function(x, y, w, h) {
    grid.rect(x, y, w-unit*0.33, h-unit(0.948, "pt"), 
              gp = gpar(fill = col["Amplification"], col = NA))
  },
  # big darkorchid2
  Deletion = function(x, y, w, h) {
    grid.rect(x, y, w-unit*0.33, h-unit(0.948, "pt"), 
              gp = gpar(fill = col["Deletion"], col = NA))
  }
)

alter_fun = list(
  background = alter_graphic("rect", fill = "#CCCCCC"),
  Missense = alter_graphic("rect", fill = col.Onco["Missense"]),
  Truncating = alter_graphic("rect", height = 0.33, fill = col.Onco["Truncating"]),
  Splicing = alter_graphic("rect", fill = col.Onco["Splicing"]),
  Amplification = alter_graphic("rect", width = 0.33, fill = col.Onco["Amplification"]),
  Deletion = alter_graphic("rect", width = 0.33, fill = col.Onco["Deletion"])
)

column_title = "Altered in 13 of 13 BPDCN samples"
heatmap_legend_param = list(title = "Alternations", at = c("Missense", "Truncating", "Splicing", "Amplification", "Deletion"), 
                            labels = c("Missense", "Truncating", "Splicing", "Amplification", "Deletion"))

pdf('~/Desktop/231205.BPDCN.Oncoprint.pdf', height=15)
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
     # row_split = rep(c("Cell proliferation", "DNA repair", "Chromatin remodeling", "Wnt pathway","Apoptosis"),c(9,10,10,5,5)),
     row_gap = unit(100, "mm"))
dev.off()
#------------------------------------------------------------------------------------------------------------------------------------#

library(ComplexHeatmap)
library(readxl)
library(dplyr)
library(readxl)

Annotation <- read.table('/Users/lee/Documents/05.대학원/01.BPDCN/03.Table/230825.BPDCN.Involve.Site.txt',
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

Onco.Data <- read_excel('~/Desktop/231205.BPDCN.Oncoprint.xlsx',
                        sheet='OncoPrint')
Onco.Data <- as.data.frame(Onco.Data)
Onco.Data <- Onco.Data[order(-rowSums(!is.na(Onco.Data))), ]
Onco.Data[is.na(Onco.Data)] <- ''
# Onco.Data <- Onco.Data[,c(1,5,4,6,10,13,12,11,9,8,2,3,7,14)]
# colnames(Onco.Data)
# rownames(Onco.Data) <- Onco.Data[,1]
# Onco.Data <- Onco.Data[,-1]

# call functional annotation data
Function <- read_excel('~/Desktop/BPDCN.Pathway.xlsx',
                       sheet = 'main')
Function <- as.data.frame(Function)

DNA_meta <- Function[1,8]
DNA_meta <- unlist(strsplit(DNA_meta, ','))

Chromatin <- Function[4,8]
Chromatin <- unlist(strsplit(Chromatin, ','))

hema <- Function[7,8]
hema <- unlist(strsplit(hema, ','))
  
cycle <- Function[11,8]
cycle <- unlist(strsplit(cycle, ','))

immune <- Function[19,8]
immune <- unlist(strsplit(immune, ','))
#------------------------------------------------------------------------------#
Diff1 <- c(DNA_meta, Chromatin)
Diff2 <- c(DNA_meta, Chromatin, hema)
Diff3 <- c(DNA_meta, Chromatin, hema, cycle)
#------------------------------------------------------------------------------#
Chromatin <- setdiff(Chromatin, DNA_meta)
hema <- setdiff(hema, Diff1)
cycle <- setdiff(cycle, Diff2)
immune <- setdiff(immune, Diff3)
#-------------------------------------------------------------------------------#
DNA_meta <- Onco.Data %>%
  filter(Gene %in% DNA_meta)
rownames(DNA_meta) <- DNA_meta$Gene
DNA_meta <- DNA_meta[-1]

Chromatin <- Onco.Data %>%
  filter(Gene %in% Chromatin)
rownames(Chromatin) <- Chromatin$Gene
Chromatin <- Chromatin[-1]

hema <- Onco.Data %>%
  filter(Gene %in% hema)
rownames(hema) <- hema$Gene
hema <- hema[-1]

cycle <- Onco.Data %>%
  filter(Gene %in% cycle)
rownames(cycle) <- cycle$Gene
cycle <- cycle[-1]

immune <- Onco.Data %>%
  filter(Gene %in% immune)
rownames(immune) <- immune$Gene
immune <- immune[-1]

Onco.Data <- rbind(DNA_meta, Chromatin, hema, immune)

dim(DNA_meta)
dim(Chromatin)
dim(hema)
dim(immune)

pdf('~/Desktop/231010.BPDCN.Oncoprint.function.pdf', height=18)
a <- oncoPrint(Onco.Data,
               alter_fun = alter_fun, col = col.Onco,
               gap = unit(c(1.5), "mm"),
               column_title = column_title, heatmap_legend_param = heatmap_legend_param,
               pct_side = "right", row_names_side = "left",
               alter_fun_is_vectorized = FALSE,
               bottom_annotation = ha,
               column_order = colnames(Onco.Data),
               row_names_gp = gpar(fontsize=5, fontface='italic'),
               pct_gp = gpar(fontsize=7),
               row_title_gp = gpar(fontsize=10))
draw(a, heatmap_legend_side = "bottom", annotation_legend_side = "bottom", merge_legend = TRUE,
     row_split = rep(c("DNA metabolic pathway",
                       "Chromatin organazation",
                       "Hematopoiesis",
                       'Immun system'),
                     c(60, 12, 10, 6)))
dev.off()
