#! python

import os

home = os.path.dirname(os.path.realpath(__file__))
exec(open(home+'/../lib/functions.py', 'r').read())

# simulate contigs and get gene content profile and kmer frequency
for i in os.listdir('gcp_vs_kmer/genbank/bacteria/'):
    genome = [j for j in os.listdir('gcp_vs_kmer/genbank/bacteria/'+i) if j.split('.')[-1] == 'fna'][0]
    # simulate contigs
    recs = list(SeqIO.parse('gcp_vs_kmer/genbank/bacteria/'+i+'/'+genome, 'fasta'))
    simu = simu_contigs(i, recs)
    outfile = open('gcp_vs_kmer/genbank/bacteria/'+i+'/simulated_contigs.fas', 'w')
    for rec in simu:
        SeqIO.write(rec, outfile, 'fasta')
    outfile.close()

    gcp = gene_content_profile('gcp_vs_kmer/genbank/bacteria/'+i+'/simulated_contigs.fas', prodigal, 'database/database.dmnd')
    gcp.to_csv('gcp_vs_kmer/genbank/bacteria/'+i+'/simu_gene_content.txt', sep='\t')

    for k in range(3,9):
        kmer = kmerFreq(simu, k=k)
        kmer.to_csv('gcp_vs_kmer/genbank/bacteria/'+i+'/simu_kmer_'+str(k)+'.txt', sep='\t')

# concat dataframes
def concat(l):
    df = pd.DataFrame()
    for i in l:
        df1 = pd.read_csv(i, sep='\t', header=0, index_col=0)
        df = pd.concat([df,df1])

    return(df)

l = ['simu_kmer_4.txt', 'simu_kmer_7.txt', 'simu_kmer_6.txt', 'simu_kmer_8.txt', 'simu_kmer_3.txt', 'simu_gene_content.txt', 'simu_kmer_5.txt']
l2 = os.listdir('gcp_vs_kmer/genbank/bacteria')
for i in l:
    df = concat(['gcp_vs_kmer/genbank/bacteria/'+j+'/'+i for j in l2])
    df = df.fillna(0)
    df.to_csv('gcp_vs_kmer/'+i, sep='\t')


