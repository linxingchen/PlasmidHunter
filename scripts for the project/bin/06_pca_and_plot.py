#! python

import pandas as pd
from sklearn.decomposition import PCA
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('gcp_vs_kmer/simu_kmer_3.txt', sep='\t', header=0, index_col=0)

dict1 = {'chro':'Chromosome', 'plas':'Plasmid'}
dict2 = {'GCA_000008865.2':'Escherichia coli', 'GCA_009363835.1':'Bacillus subtilis','GCA_019738995.1':'Pseudomonas aeruginosa'}

df1 = pd.DataFrame(index=df.index)
df1['location'] = [dict1[i.split('|')[3]] for i in df.index]
df1['taxon'] = [dict2[i.split('|')[2]] for i in df.index]
df1['length'] = [int(i.split('|')[4].split('bp')[0]) for i in df.index]

l = os.listdir('gcp_vs_kmer/')
l = [i for i in l if i[:4] == 'simu']
dict3 = {}

for i in l:
    df = pd.read_csv('gcp_vs_kmer/'+i, sep = '\t', header = 0, index_col = 0)
    ar = np.array(df)
    pca = PCA(2).fit_transform(ar)
    pca = pd.DataFrame(pca, index = df.index, columns = ['PC1', 'PC2'])
    pca = pd.concat([pca, df1], axis=1)
    pca.to_csv('gcp_vs_kmer/pca_'+i, sep='\t')
    dict3[i] = pca

# plotting
dict4 = {i:dict3[i] for i in ['simu_kmer_4.txt', 'simu_kmer_5.txt', 'simu_kmer_6.txt', 'simu_gene_content.txt']}

fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize=(10,6))

for i, j, k in zip(list(dict4.items())[:4], [ax1, ax2, ax3, ax4], ['A', 'B', 'C', 'D']):
    g = sns.scatterplot(data=i[1], x='PC1', y='PC2', hue='location', style='taxon', markers=['o', 's', '^'], size='length', alpha=0.2, legend=(), ax=j)
    g.set(title=' '.join(i[0][5:-4].split('_')))
    g.set_title(k, loc='left')

g = sns.scatterplot(data=i[1], x='PC1', y='PC2', hue='location', style='taxon', markers=['o', 's', '^'], size='length', alpha=0.2, ax=ax5) # enlarged gene content plot
ax5.set_title(' '.join(i[0][5:-4].split('_'))+' (zoomed in)', fontsize=10, loc='right')
ax5.set_xlim(-0.7, 0)
ax5.set_ylim(-0.7, 0)
ax5.set_title('E', loc='left')

ax6.axis('off')
ax5.legend(loc=(1.5, -0.1), prop={'size':8})

plt.subplots_adjust(wspace=0.5, hspace=0.5)
fig.savefig('gcp_vs_kmer/scatterplot.pdf')
