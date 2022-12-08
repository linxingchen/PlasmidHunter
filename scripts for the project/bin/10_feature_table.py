#! python

exec(open('scripts/lib/functions.py', 'r').read())
import pickle

dna_file = 'modeling/contigs/simulated_contigs.fasta'
prodigal_func = prodigal
database = 'database/database.dmnd'
cpu = 100

df = gene_content_profile(dna_file, prodigal_func, database, cpu=cpu)
df = df.loc[df.sum(axis=1)>5, :]
df = df.loc[:,df.sum()>0]
df.to_pickle('modeling/training_data.pkl')
pickle.dump(df.columns, open('modeling/feature_genes.pkl', 'wb'))

