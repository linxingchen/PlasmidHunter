#! python
# This script removes the clusters with < n proteins and removes any repeated sequences if any. It then makes a DIAMOND database (.dmnd).

import pandas as pd
import os
from Bio import SeqIO

# read the clustering output, remove singletons (e.g. <2 seqs)
os.chdir('database')
df = pd.read_csv('mmseqs_cluster.tsv', sep='\t', header=None, index_col=None)
df = df.drop_duplicates()
df = df.set_index(0)
df[2] = [1 for i in df.index]
df1 = df.groupby(level=0).sum()
df2 = df1.loc[df1[2]>5,:] # n
open('database_summary.txt', 'w').write('Total unique proteins: '+str(df.shape[0])+'\nTotal representative proteins: '+str(df2.shape[0])+'\n')

# calculate annotation rate and write a representation table
df3 = df.loc[df2.index,[1]]
open('database_summary.txt', 'a').write('Representing '+str(df3.shape[0])+' sequences\n')
df3 = df3.reset_index().set_index(1)
json.dump(df3.to_dict()[0], open('repre.json', 'w'))

# write the reprentative sequence in database
outfile = open('database.faa', 'w')
dict1 = df2.to_dict()[2]
dict2 = {}
for rec in SeqIO.parse('mmseqs_rep_seq.fasta', 'fasta'):
    if dict1.get(rec.id) and not dict2.get(rec.id):
        dict2[rec.id] = 1
        SeqIO.write(rec, outfile, 'fasta')
outfile.close()

os.system('diamond makedb --in database.faa --db database')

os.chdir('..')

