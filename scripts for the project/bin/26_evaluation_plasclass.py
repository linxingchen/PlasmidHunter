#! python

import pandas as pd
exec(open('/home/tianrm/software/scripts/machine_learning/lib/functions.py', 'r').read())
import seaborn as sns
import glob
import json
from Bio import SeqIO

tool = 'PlasClass'
def evaluate(input_contigs, predict_out):
    y_true = {}
    for rec in SeqIO.parse(input_contigs, 'fasta'):
        y_true[rec.id] = rec.description.split(' ')[1]

    df = pd.read_csv(predict_out, sep='\t', header=None, index_col=0)

    y_true = [y_true[i] for i in df.index]
    y_true = [0 if i=='chromosome' else 1 if i=='plasmid' else 2 for i in y_true]
    
    df[0] = 1 - df[1]
    y_score = np.array(df[[0,1]])

    return(classification_evaluation(y_true, y_score))

dict1 = {}
dict2 = json.load(open('testing/benchmarking/%s/time_used' % tool, 'r'))

l = os.listdir('testing/benchmarking/%s' % tool)
l = [i for i in l if i[-4:] == 'seqs']
for i in l:
    dict1[i] = evaluate('testing/simulated_contigs/'+i, 'testing/benchmarking/'+tool+'/'+i+'/out')
    dict1[i]['time_used'] = round(dict2[i]/60, 1) 

df = pd.DataFrame.from_dict(dict1).transpose()
df['contig length'] = [i.split('_')[0] for i in df.index]
df.index = [int(i.split('k')[0]) for i in df.index]
df = df.sort_index()
df.drop('roc', axis=1).to_csv('testing/benchmarking/%s/evaluation.tsv' % tool, sep='\t')

