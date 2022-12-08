#! python

import matplotlib.pyplot as plt
import pickle
import pandas as pd
import seaborn as sns

# save the model
out = pickle.load(open('modeling/out.pkl', 'rb'))
pickle.dump(out['GaussianNB()']['bestModel'], open('modeling/guassiannb.pkl', 'wb')) # the best model
pickle.dump(out['LogisticRegression()']['bestModel'], open('modeling/logisticregression.pkl', 'wb')) # the best model
# plotting
dict1 = {i:out[i]['evaluation'] for i in out}
df = pd.DataFrame.from_dict(dict1).transpose()
df['methods'] = ['RF', 'DT', 'NB', 'LR', 'PCA-RF', 'PCA-DT', 'PCA-NB', 'PCA-LR', 'PCA-KNN']
df.drop('roc', axis=1).to_csv('modeling/evaluation.tsv', sep='\t')

fig, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) = plt.subplots(3, 3, figsize=(9, 8))

for i,j,k,l in zip(df.columns[:7], [ax1, ax2, ax3, ax4, ax5, ax6, ax7], ['Accuracy', 'Balanced Accuracy','Log Loss', 'Recall', 'Precision', 'F Score', 'ROC AUC'], list('ABCDEFG')):
    g = sns.barplot(data=df, x='methods', y=i, ax=j)
    g.set(xticklabels=[])
    g.set(xlabel=None)
    g.set_title(k, fontsize=10)
    g.set_title(l, loc='left')

for i in df.index:
    ax8.plot(df.loc[i,'roc'][0],df.loc[i,'roc'][1], label=df.loc[i,'methods'])

ax8.set_title('ROC', fontsize=10)
ax8.set_title('H', loc='left')

ax9.axis('off')
fig.legend(title='Methods', loc=(0.75,0.08), prop={'size':10})
plt.subplots_adjust(wspace=0.5, hspace=0.5)
fig.savefig('modeling/evaluation.pdf')

