#! python

import json
import random
from collections import Counter
import os
import pandas as pd
import pickle
import time
from multiprocessing.pool import Pool
from Bio import SeqIO
import gzip

# download DNA sequences
print('Downloading all fna files ...')
df = pd.read_csv('scripts/lib/prokaryotes.csv', header = 0, index_col = 0)
os.system('rm -rf modeling/fna; mkdir modeling/fna')
os.chdir('modeling/fna')

def download(url):
    time.sleep(0.5)
    os.system('wget '+url+'/'+url.split('/')[-1]+'_genomic.fna.gz')

pool = Pool(20)
for i in df['RefSeq FTP']:
    pool.apply_async(download, (i,))

pool.close()
pool.join()

os.chdir('../../')

# read the amplicon and type data
print('Reading the gff.json and screen for plasmids and chromosomes with > 5000 bp')
dict1 = json.loads(open('modeling/gff.json', 'r').read())
p = [i for i in dict1 if dict1[i]['loc']=='plasmid' and dict1[i]['size'] > 5000]
c = [i for i in dict1 if dict1[i]['loc']=='chromosome' and dict1[i]['size'] > 5000]

# sampling amplicons randomly
print('Randomly select 15000 sequences for training, save the rest sequence ids for validation')
s = 1
random.seed(s)
p1 = random.sample(p, 15000)
p2 = set(p) - set(p1)
json.dump(list(p2), open('modeling/testing_acc_p.json', 'w')) # accesion IDs for testing and evaluation data set

random.seed(s)
c1 = random.sample(c, 15000)
c2 = set(c) - set(c1)
json.dump(list(c2), open('modeling/testing_acc_c.json', 'w')) # accesion IDs for testing and evaluation data set

# sampling contigs randomly
def random_contig(rec, t, mini=5000, maxi=100000):
    seq = rec.seq + rec.seq
    random.seed(rec.id)
    start = random.randint(0, len(seq)/2)
    random.seed(rec.id)
    length = random.randint(mini, min(maxi, len(seq)/2))
    end = start + length
    rec.seq = seq[start:end]
    rec.id += '-'+t
    rec.description = 'start=%d length=%d' % (start, length)
    
    return(rec)

os.system('rm -rf modeling/contigs; mkdir modeling/contigs')
outfile = open('modeling/contigs/simulated_contigs.fasta', 'w')
for f in os.listdir('modeling/fna/'):
    try:
        for rec in SeqIO.parse(gzip.open('modeling/fna/'+f, 'rt'), 'fasta'):
            if rec.id in p1 or rec.id in c1:
                rec = random_contig(rec, dict1[rec.id]['loc'], mini=5000, maxi=100000)
                SeqIO.write(rec, outfile, 'fasta')
    except:
        pass

outfile.close()

