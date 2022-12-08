#! python

import os
import sys
import subprocess as subp
from multiprocessing import Pool
import pandas as pd
import numpy as np
import random
import json
from random import randint
from collections import Counter
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.SeqFeature import SeqFeature
from Bio.SeqFeature import FeatureLocation

def call(cmd='',out='',err=''):
    if subp.call('set -ex; '+cmd,shell=True)==0:
        print('\n'+out+'\n')
    else:
        print('\n'+err+'\n')
        sys.exit(1)

def split_fasta(infile, outdir, n=10):
    print('Now splitting input fasta file ...')
    dict1 = SeqIO.to_dict(SeqIO.parse(infile, 'fasta'))
    ids = dict1.keys()
    split = np.array_split(list(ids), n)
    for i in range(len(split)):
        outfile = open('%s/%d.fasta' % (outdir, i), 'w')
        for j in split[i]:
            SeqIO.write(dict1[j], outfile, 'fasta')
        outfile.close()

def prodigal(indir, f):
    call('prodigal -a %s/%s.faa -o %s/%s.out -i %s/%s -p meta -q' % (indir, f, indir, f, indir, f), 'Prodigal prediction for %s completed.' % f, 'Prodigal prediction for %s failed.' % f)
 
def prodigal_predict(indir, prodigal_func):
    print('Now predicting protein sequences using Prodigal ...')
   
    files = [i for i in os.listdir(indir) if i.split('.')[-1] == 'fasta']
    pool = Pool(len(files))
    for f in files:
        pool.apply_async(prodigal_func, (indir, f,))
    pool.close()
    pool.join()

def diamond_alignment(query, database, cpu=10): 
    print('Now aligning protein sequences against database using Diamond ...')
    call('diamond blastp --query '+query+' --max-target-seqs 1 --max-hsps 1 --evalue 1e-5 --id 40 --query-cover 80 --db '+database+' --out '+query+'.daa --outfmt 6 --threads '+str(cpu), 'Diamond alignment completed.', 'Diamond alignment failed.')

def daa_to_hits(daa):
    print('Now parsing Diamond alignment results ...')
    dict1 = {}
    df = pd.read_csv(daa, sep = '\t', header = None, index_col = 0)
    df = df.loc[:,1]
    df.index = ['_'.join(i.split('_')[:-1]) for i in df.index]
    dict1 = df.groupby(level=0).apply(list).to_dict()

    return(dict1)

def list_to_df(li1, name):
    dict1 = Counter(li1)
    df = pd.DataFrame({name: dict1})
    df[df>0] = 1
    
    return(df)

def gene_content_profile(dna_file, prodigal_func, database, cpu=10): # get gene content profile of sequences using a diamond output
    temp_dir = dna_file+'_temp'
    os.system('rm -rf %s; mkdir %s' % (temp_dir, temp_dir))
    split_fasta(dna_file, temp_dir, n=cpu)
    prodigal_predict(temp_dir, prodigal_func)
    os.system('cat %s/*.faa > %s/proteins.faa' % (temp_dir, temp_dir))
    diamond_alignment(temp_dir+'/proteins.faa', database, cpu=cpu)
    dict1 = daa_to_hits(temp_dir+'/proteins.faa.daa')

    print('Now generating gene content profile ...')
    df = pd.concat([list_to_df(dict1[i], i) for i in dict1], axis=1)
    df = df.fillna(0)
    df = df.transpose()
    os.system('rm -rf %s' % temp_dir)

    return(df)

def simu_contigs(strain, recs, length='random', lower=5000, upper=100000, num=100, seed=1):
    simu = []
    for rec in recs:
        l = len(rec.seq)
        if l > 500000:
            loc = 'chro'
        else:
            loc = 'plas'
        # skip if sequence length too short
        if length == 'random' and l < lower:
            continue
        elif length != 'random' and l < length:
            continue

        seq = rec.seq+rec.seq
        for i in range(num):
            # set start point
            random.seed(seed+i)
            start = randint(0,l-1)
            # set end point
            if length == 'random':
                random.seed(seed+i+1)
                # if l < 100k, upper limit is l
                l2 = randint(lower, np.min([l,upper]))
            else:
                l2 = length

            end = start + l2
            strand = random.choice([1,-1])
            s = SeqFeature(FeatureLocation(start, end, strand=strand)).extract(seq)
            simu.append(SeqRecord(id=rec.id+'|#'+str(i)+'|'+strain+'|'+loc+'|'+str(l2)+'bp|'+str(strand), seq=s))

    return(simu)

def kmerFreq(recs, k=4):
    def kmerDict(seq, k=4):
        list1 = []
        for i in range(0, len(seq)-3):
            list1.append(seq[i:i+k])
        return(Counter(list1))

    dict1 = {}
    for rec in recs:
        dict1[rec.id] = kmerDict(str(rec.seq), k=k)
    df = pd.DataFrame.from_dict(dict1)
    df = df/df.sum()
    return(df.transpose().fillna(0))


def random_sub_list(li1, n, length='random', seed=1):
    l = len(li1)
    li2 = li1.copy()
    li2.extend(li2)
    li = []
    for i in range(n):
        random.seed(i+seed)
        start = randint(0,l-1)
        if length == 'random':
            random.seed(i+seed+1)
            step = randint(1,l)
        elif length > l:
            return()
        else:
            step = length
        li3 = li2[start:start+step]
        li.append(li3)
    
    return(li)





