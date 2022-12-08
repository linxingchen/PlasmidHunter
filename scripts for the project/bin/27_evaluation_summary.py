#! python

import re
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

df1 = pd.DataFrame()

for i in ['PlasmidHunter', 'PlasClass', 'PlasForest', 'Deeplasmid', 'PlasmidVerify', 'PlasFlow']:
    df = pd.read_csv('testing/benchmarking/%s/evaluation.tsv' % i, sep='\t', header=0, index_col=0)
    df['contig length'] = [re.sub(r'kbp', '', i) for i in df['contig length']]
    df['tool'] = [i] * df.shape[0]
    df1 = pd.concat([df1, df])

df1 = df1.reset_index()

fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize=(8, 5))

for i,j,k,l in zip(['accuracy', 'recall', 'precision', 'f_score', 'time_used'], [ax1, ax2, ax3, ax4, ax5], ['Accuracy', 'Recall', 'Precision', 'F score', 'Time used (min)'], list('ABCDE')):
    g = sns.lineplot(data=df1, x='contig length', y=i, hue='tool', legend=False, ax=j)
    g.set_xlabel('contig length (Kbp)', size=8)
    if i=='time_used':
        g.set(yscale='log')
    if i in ['accuracy', 'precision']:
        g.set_ylim(0.5)
    g.set_title(k, fontsize=10)
    g.set_title(l, loc='left')

df1['a'] = 0
g = sns.barplot(data=df1, x='contig length', y='a', hue='tool', ax=ax6)
ax6.axis('off')

plt.legend(title='Tools', loc=(0.01,0.05), prop={'size':10})
plt.subplots_adjust(wspace=0.5, hspace=0.5)
fig.savefig('testing/benchmarking/evaluation.pdf')

