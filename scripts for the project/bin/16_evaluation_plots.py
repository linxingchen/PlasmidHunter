#! python

import pandas as pd
exec(open('/home/tianrm/software/scripts/machine_learning/lib/functions.py', 'r').read())
from Bio import SeqIO
import seaborn as sns
import matplotlib.pyplot as plt
import json

def evaluate(input_contigs, predictions):
    y_true = {}
    for rec in SeqIO.parse(input_contigs, 'fasta'):
        y_true[rec.id] = rec.description.split(' ')[1]
    
    df = pd.read_csv(predictions, sep='\t', header=0, index_col=0)
    y_score = np.array(df.iloc[:,1:])
    
    y_true = [y_true[i] for i in df.index]
    y_true = [0 if i=='chromosome' else 1 if i=='plasmid' else 2 for i in y_true]

    return(classification_evaluation(y_true, y_score))

dict1 = {}
dict2 = json.load(open('testing/benchmarking/PlasmidHunter/time_used', 'r'))

for i in os.listdir('testing/simulated_contigs/'):
    dict1[i] = evaluate('testing/simulated_contigs/'+i, 'testing/benchmarking/PlasmidHunter/'+i+'/predictions.tsv')
    dict1[i]['time_used'] = round(dict2[i]/60, 1)

df = pd.DataFrame.from_dict(dict1).transpose()
df['contig length'] = [i.split('_')[0] for i in df.index]
df.index = [int(i.split('k')[0]) for i in df.index]
df = df.sort_index()
df.drop('roc', axis=1, inplace=True)
df.to_csv('testing/benchmarking/PlasmidHunter/evaluation.tsv', sep='\t')

fig, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) = plt.subplots(3, 3, figsize=(7, 6))

for i,j,k,l in zip(df.columns[:8], [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8], ['Accuracy', 'Bal. Accuracy','Log Loss', 'Recall', 'Precision', 'F Score', 'ROC AUC', 'Time (min)'], list('ABCDEFGH')):
    g = sns.barplot(data=df, x='contig length', y=i, ax=j)
    g.set(xticklabels=[])
    g.set(xlabel=None)
    g.set_title(k, fontsize=10)
    g.set_title(l, loc='left')
    plt.legend([], [], frameon=False)

df['a'] = 0
g = sns.barplot(data=df, x='contig length', y='a', hue='contig length', ax=ax9)
ax9.axis('off')

plt.legend(title='Contig length', loc=(0.1,0.05), prop={'size':10})
plt.subplots_adjust(wspace=0.5, hspace=0.5)
fig.savefig('testing/benchmarking/PlasmidHunter/evaluation.pdf')

