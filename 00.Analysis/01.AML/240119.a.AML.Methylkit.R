#라이브러리 호출
library(methylKit)
library(genomation)
library(annotatr)

#경로 설정 및 파일 호출
setwd('/media/node01-HDD01/00.AML/00.Case/')
file.list <-list('CR_AYB_8571482_S13.deduplicated.bismark.cov',
                 'CR_HJJ_8078629_S4.deduplicated.bismark.cov',
                 'CR_JJB_1448093_S19.deduplicated.bismark.cov',
                 'CR_JTN_8726498_S17.deduplicated.bismark.cov',
                 'CR_KDS_10184967_S23.deduplicated.bismark.cov',
                 'CR_KYK_4081216_S7.deduplicated.bismark.cov',
                 'CR_LJP_5782145_S15.deduplicated.bismark.cov',
                 'CR_LKB_4001150_S24.deduplicated.bismark.cov',
                 'CR_LKH_10092375_S21.deduplicated.bismark.cov',
                 'CR_NKYY_8349009_S11.deduplicated.bismark.cov',
                 'CR_SYK_3707712_S9.deduplicated.bismark.cov',
                 'CR_YSJ_4357702_S1.deduplicated.bismark.cov',
                 'NR_HSW_6007706_S12.deduplicated.bismark.cov',
                 'NR_JMJ_8215717_S3.deduplicated.bismark.cov',
                 'NR_JWS_2085936_S14.deduplicated.bismark.cov',
                 'NR_KKY_8360201_S16.deduplicated.bismark.cov',
                 'NR_KWH_2119463_S5.deduplicated.bismark.cov',
                 'NR_KYS_8666745_S10.deduplicated.bismark.cov',
                 'NR_LHB_5691112_S18.deduplicated.bismark.cov',
                 'NR_LMS_8718125_S20.deduplicated.bismark.cov',
                 'NR_PHS_4372529_S6.deduplicated.bismark.cov',
                 'NR_PMK_BM_5394444_S8.deduplicated.bismark.cov',
                 'NR_SWSJ_7143657_S22.deduplicated.bismark.cov',
                 'NR_YDM_PB_4144604_S2.deduplicated.bismark.cov')


#Methylkit Run
Data <- methRead(file.list,
                 sample.id = list('CR_AYB',
                                  'CR_HJJ',
                                  'CR_JJB',
                                  'CR_JTN',
                                  'CR_KDS',
                                  'CR_KYK',
                                  'CR_LJP',
                                  'CR_LKB',
                                  'CR_LKH',
                                  'CR_NKYY',
                                  'CR_SYK',
                                  'CR_YSJ',
                                  'NR_HSW',
                                  'NR_JMJ',
                                  'NR_JWS',
                                  'NR_KKY',
                                  'NR_KWH',
                                  'NR_KYS',
                                  'NR_LHB',
                                  'NR_LMS',
                                  'NR_PHS',
                                  'NR_PMK',
                                  'NR_SWSJ',
                                  'NR_YDM'),
                 assembly = 'hg19',
                 treatment=rep(c(0,1),c(12,12)),
                 context='CpG',
                 mincov=1,
                 resolution='base',
                 pipeline='bismarkCoverage')

normalizedData <- normalizeCoverage(Data, 
                                    method="mean",
                                    chunk.size = 1e8,
                                    save.db = F)

TiledData <- tileMethylCounts(normalizedData, 
                             win.size=150, 
                             step.size=150, 
                             cov.bases=1,
                             mc.cores=20,
                             save.db = F)

MergedData <- unite(TiledData, 
                    destrand = F,
                    chunk.size = 1e8,
                    mc.cores = 20,
                    save.db = T)

Data <- data.frame(MergedData)

write.table(MergedData, '240119.AML.150bp.txt', sep='\t')

DiffData <- calculateDiffMeth(MergedData,
                              mc.cores = 20,
                              chunk.size = 1e8,
                              save.db = F)
#------------------------------------------------------------------------------#

#DMR 추출
setwd('/labmed/08.AML/02.WGBS/12.1128/')
Hyper.diffData <- getMethylDiff(DiffData, difference = 0, qvalue = 0.05, type = "hyper",chunk.size = 1e8)
write.table(Hyper.diffData, '1114.Methylkit.Hyper.txt', sep='\t', quote=F, col.names=T, row.names=F)

Hypo.diffData <- getMethylDiff(DiffData, difference = 0, qvalue = 0.05, type = "hypo",chunk.size = 1e8)
write.table(Hypo.diffData, '1114.Methylkit.Hypo.txt', sep='\t', quote=F, col.names=T, row.names=F)

All.diffData <- getMethylDiff(DiffData, difference = 0, qvalue = 0.05, chunk.size = 1e8)
write.table(All.diffData, '1128.Methylkit.1000W.ALL.txt', sep='\t', quote=F, col.names=T, row.names=F)

Hyper <- read.table('1114.Methylkit.Hyper.txt', header=T)
Hyper$DM_status <- 'hyper'
colnames(Hyper) <- c('chr','start','end','strand','pvalue', 'qvalue','meth.diff', 'DM_status')
Hyper <- Hyper[,c(1,2,3,8,6,4,7)]
write.table(Hyper, '1114.Methylkit.Hyper.comp.txt', row.names = FALSE, col.names=FALSE, quote=FALSE, sep='\t')

Hypo <- read.table('1114.Methylkit.Hypo.txt', header=T)
Hypo$DM_status <- 'hypo'
colnames(Hypo) <- c('chr','start','end','strand','pvalue', 'qvalue','meth.diff', 'DM_status')
Hypo <- Hypo[,c(1,2,3,8,6,4,7)]
write.table(Hypo, '1114.Methylkit.Hypo.comp.txt',row.names = FALSE, col.names=FALSE, quote=FALSE, sep='\t')

All <- rbind(Hyper, Hypo)
write.table(All, '1114.Methylkit.All.comp.txt',row.names = FALSE, col.names=FALSE, quote=FALSE, sep='\t')

#------------------------------------------------------------------------------#
# pdf('0812.Diff.Chr.pdf')
# diffMethPerChr(DiffData, plot=TRUE, qvalue.cutoff=0.01, meth.cutoff=20)
# dev.off()
#------------------------------------------------------------------------------#
gene.obj <- readTranscriptFeatures("/Bioinformatics/01.Reference/hg19/Methylation/refseq.hg19.bed")

DiffAnn <- annotateWithGeneParts(as(All.diffData,"GRanges"),gene.obj)
Anno <- (getAssociationWithTSS(DiffAnn))


as(All.diffData,"GRanges")
All.diffData$TSS_Distance <- Anno$dist.to.feature 
All.diffData$NM <- Anno$feature.name
All.diffData$strand <- Anno$feature.strand

write.table(All.diffData, '1128.Methyl.All.TSS.DMR.txt', row.names = F, col.names = F, quote = F, sep='\t')

unique(Anno$feature.name)
write.table(unique(Anno$feature.name), '1128.NM.txt', row.names = F, col.names = F, quote = F, sep='\t')
#------------------------------------------------------------------------------#
#DMR Annotation
#주의 사항 chr1~chrX,Y 이외 나머지 chr이 DMR에 있을경우 Error발생
library(annotatr)
setwd("/labmed/08.AML/02.WGBS/12.1128/")

dm_file = system.file("/labmed/08.AML/02.WGBS/11.DMR/01.Methylkit/",
                      '1114.Methylkit.All.comp.txt', 
                      package = 'annotatr')

dm_file='1114.Methylkit.All.comp.txt'
extraCols = c(diff_meth = 'numeric')
dm_regions = read_regions(con = dm_file, genome = 'hg19', extraCols = extraCols, format = 'bed',
                          rename_name = 'DM_status', rename_score = 'pval')

annots = c('hg19_cpgs', 'hg19_basicgenes', 'hg19_genes_intergenic',
           'hg19_genes_intronexonboundaries')

annotations = build_annotations(genome = 'hg19', annotations = annots)

dm_annotated = annotate_regions(regions = dm_regions,
                                annotations = annotations,
                                ignore.strand = TRUE,
                                quiet = FALSE)

df_dm_annotated = data.frame(dm_annotated)
print(head(df_dm_annotated))

Save <- write.table(df_dm_annotated, '1114.Methylkit.annotate.txt', sep ='\t', quote = F, col.names = T)


#Annotate region 
annots_order = c(
  'hg19_genes_1to5kb',
  'hg19_genes_promoters',
  'hg19_genes_5UTRs',
  'hg19_genes_exons',
  'hg19_genes_intronexonboundaries',
  'hg19_genes_introns',
  'hg19_genes_3UTRs',
  'hg19_genes_intergenic')

dm_vs_kg_annotations = plot_annotation(
  annotated_regions = dm_annotated,
  annotation_order = annots_order,
  plot_title = ' ',
  x_label = ' ',
  y_label = 'Count')

dm_vs_coannotations = plot_coannotations(
  annotated_regions = dm_annotated,
  annotation_order = annots_order,
  axes_label = '',
  plot_title = '')

#Annotate CpG region
x_order = c(
  'hyper',
  'hypo')

fill_order = c(
  'hg19_cpg_islands',
  'hg19_cpg_shores',
  'hg19_cpg_shelves',
  'hg19_cpg_inter')

dm_vs_cpg_cat1 = plot_categorical(
  annotated_regions = dm_annotated, x='DM_status', fill='annot.type',
  x_order = x_order, fill_order = fill_order, position='stack',
  plot_title = '',
  legend_title = 'Annotations',
  x_label = '',
  y_label = 'Count')

x_order = c(
  'hg19_genes_1to5kb',
  'hg19_genes_promoters',
  'hg19_genes_5UTRs',
  'hg19_genes_exons',
  'hg19_genes_intronexonboundaries',
  'hg19_genes_introns',
  'hg19_genes_3UTRs',
  'hg19_genes_intergenic')

fill_order = c(
  'hyper',
  'hypo')

dm_vs_kg_cat = plot_categorical(
  annotated_regions = dm_annotated, x='annot.type', fill='DM_status',
  x_order = x_order, fill_order = fill_order, position='fill',
  legend_title = '',
  x_label = '',
  y_label = 'Proportion')

pdf('/labmed/08.AML/00.Data/02.Plots/0907.DMR.Stats.pdf')
dm_vs_kg_annotations
dm_vs_coannotations
dm_vs_cpg_cat1
dm_vs_kg_cat
dev.off()

dm_annsum = summarize_annotations(
  annotated_regions = dm_annotated,
  quiet = TRUE)
print(dm_annsum)

write.table(dm_annsum, '0907.Methylkit.All.stats.txt', sep='\t', quote=F, 
            col.names = F,
            row.names = F)
dm_catsum = summarize_categorical(
  annotated_regions = dm_annotated,
  by = c('annot.type', 'DM_status'),
  quiet = TRUE)
print(dm_catsum)
write.table(dm_catsum, '0907.Methylkit.CpG.stats.txt', sep='\t', quote=F, 
            col.names = F,
            row.names = F)
