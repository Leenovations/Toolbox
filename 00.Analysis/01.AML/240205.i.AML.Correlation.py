import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#---------------------------------------------------------------------------#
AML = pd.read_csv('/labmed/01.AML/AML.Correlation.txt',
                  sep='\t',
                  header='infer')

Index = pd.Series(AML.iloc[:,0]).tolist()
AML.index = Index
AML = AML.drop('Sample', axis=1)

colormap = plt.cm.gist_heat
plt.figure(figsize=(15,12))
sns.set(font_scale=1)
sns.heatmap(AML.corr(), linewidths=0.1, vmax=0.5, cmap=colormap, linecolor='white', annot=True)
plt.xticks(ha='right', rotation=90)
plt.yticks(ha='right', rotation=0)
plt.savefig('/labmed/01.AML/04.Results/00.Plots/Correlation.png')