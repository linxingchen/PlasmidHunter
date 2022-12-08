#! python

import pandas as pd
exec(open('/home/tianrm/software/scripts/machine_learning/lib/functions.py', 'r').read())
import seaborn as sns
import glob
import json

def evaluate(predict_out):
    out = open(predict_out, 'r').readlines()
    out.pop(0)
    y_true = [i.split(' ')[1] for i in out]
    y_true = [0 if i=='chromosome' else 1 if i=='plasmid' else 2 for i in y_true]
    y_score = [float(i.split(',')[2].split(' ')[0]) for i in out]
    y_score = [[1-i, i] for i in y_score]

    return(classification_evaluation(y_true, y_score))

dict1 = {}
dict2 = json.load(open('testing/benchmarking/Deeplasmid/time_used', 'r'))

l = os.listdir('testing/benchmarking/Deeplasmid')
l = [i for i in l if i[-4:] == 'seqs']
for i in l:
    dict1[i] = evaluate(glob.glob('testing/benchmarking/Deeplasmid/'+i+'/outPR*/predictions.txt')[0])
    dict1[i]['time_used'] = round(dict2[i]/60, 1) 

df = pd.DataFrame.from_dict(dict1).transpose()
df['contig length'] = [i.split('_')[0] for i in df.index]
df.index = [int(i.split('k')[0]) for i in df.index]
df = df.sort_index()
df.drop('roc', axis=1).to_csv('testing/benchmarking/Deeplasmid/evaluation.tsv', sep='\t')

