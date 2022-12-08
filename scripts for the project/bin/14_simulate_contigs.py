#! python

import os
import random
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
home = os.path.dirname(os.path.realpath(__file__))
exec(open(home+'/../lib/functions.py', 'r').read())

def random_contig(rec, length, t, seed=0):
    seq = rec.seq
    if len(seq) < length:
        return()

    random.seed(seed)
    start = random.randint(0,len(seq))
    seq = seq + seq
    seq = seq[start:start+length]
    r = SeqRecord(seq, id=rec.id, description=t+' simulated contig '+str(len(seq))+' bp')

    return(r)

def simulate_contigs(indir, t, length):
    num = 0
    simu_recs = []

    for i in os.listdir(indir):
        num += 1
        rec = next(SeqIO.parse(indir+'/'+i, 'fasta'))
        r = random_contig(rec, length, t, seed=num)
        simu_recs.append(r)
    
    simu_recs = [i for i in simu_recs if bool(i)]

    return(simu_recs)

os.system('rm -rf testing/simulated_contigs; mkdir -p testing/simulated_contigs')

# simulate contigs
for l in [5, 10, 20, 50, 100]:
    # plasmid
    simu_recs = simulate_contigs('testing/genomes/p', 'plasmid', l*1000)
    num = len(simu_recs)

    outfile = open('testing/simulated_contigs/'+str(l)+'kbp_'+str(num)+'seqs', 'w')
    for r in simu_recs:
        SeqIO.write(r, outfile, 'fasta')
    print('plasmids: '+str(l)+' kbp, '+str(num)+' sequences written')
    
    # chromosome, the same number of contigs as plasmid
    simu_recs = simulate_contigs('testing/genomes/c', 'chromosome', l*1000)
    simu_recs = simu_recs[:num]
    num = len(simu_recs)

    for r in simu_recs:
        SeqIO.write(r, outfile, 'fasta')
    outfile.close()
    print('chromosome: '+str(l)+' kbp, '+str(num)+' sequences written')

