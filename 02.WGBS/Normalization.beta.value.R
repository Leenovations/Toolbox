# Load the required library
library(sva)

methylation_data <- read.table('/labmed/06.AML/Result/04.Normal/CpG.AML.Normal.txt', sep='\t', header=T)
methylation_data <- na.omit(methylation_data)
Position <- methylation_data[,c(1,2,3)]
methylation_data <- methylation_data[,-c(1,2,3)]
design <- data.frame(Batch = factor(c(rep(c('Batch1','Batch2'), c(24,18))))) # Add all your sample labels

# Convert your methylation data to a matrix
meth_matrix <- as.matrix(methylation_data)

# Run ComBat to normalize the data
combat_normalized_data <- ComBat(dat = meth_matrix, batch = design$Batch)

combat_normalized_data <- as.data.frame(cbind(Position, round(combat_normalized_data, digits = 2)))
write.table(combat_normalized_data, '/labmed/06.AML/Result/04.Normal/Normalized.txt',
            sep='\t',
            quote = F,
            row.names = F,
            col.names = T)

min_val <- min(combat_normalized_data[,-c(1,2,3)])
max_val <- max(combat_normalized_data[,-c(1,2,3)])
combat_normalized_scaled <- ((combat_normalized_data[,-c(1,2,3)] - min_val) / (max_val - min_val)) * 100
combat_normalized_scaled <- round(combat_normalized_scaled, digits = 2)

combat_normalized_scaled <- as.data.frame(cbind(Position, combat_normalized_scaled))
write.table(combat_normalized_scaled, '/labmed/06.AML/Result/04.Normal/Normalized.Scaled.txt',
            sep='\t',
            quote = F,
            row.names = F,
            col.names = T)
