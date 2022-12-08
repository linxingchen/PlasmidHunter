#! python

import pandas as pd
exec(open('/home/tianrm/software/scripts/machine_learning/lib/functions.py', 'r').read())
import seaborn as sns
import glob
import json
from Bio import SeqIO

def evaluate(input_contigs, predict_out):
    y_true = {}
    for rec in SeqIO.parse(input_contigs, 'fasta'):
        y_true[rec.id] = rec.description.split(' ')[1]

    out = open(predict_out, 'r').readlines()
    out.pop(0)
    y_pred= [tuple(i.split(',')[0:2]) for i in out]
    y_pred = dict(y_pred)

    y_true = [y_true[i] for i in y_pred]
    y_true = [0 if i=='chromosome' else 1 if i=='plasmid' else 2 for i in y_true]
    y_pred = list(y_pred.values())
    y_pred = [0 if i=='Chromosome' else 1 if i=='Plasmid' else 2 for i in y_pred]

    return(classification_evaluation2(y_true, y_pred))

dict1 = {}
dict2 = json.load(open('testing/benchmarking/PlasmidVerify/time_used', 'r'))

l = os.listdir('testing/benchmarking/PlasmidVerify')
l = [i for i in l if i[-4:] == 'seqs']
for i in l:
    dict1[i] = evaluate('testing/simulated_contigs/'+i, glob.glob('testing/benchmarking/PlasmidVerify/'+i+'/*result*')[0])
    dict1[i]['time_used'] = round(dict2[i]/60, 1) 

df = pd.DataFrame.from_dict(dict1).transpose()
df['contig length'] = [i.split('_')[0] for i in df.index]
df.index = [int(i.split('k')[0]) for i in df.index]
df = df.sort_index()
df.to_csv('testing/benchmarking/PlasmidVerify/evaluation.tsv', sep='\t')

