#! python

import os
import json
import time

os.system('mkdir -p testing; rm -rf testing/genomes; mkdir testing/genomes; mkdir testing/genomes/c testing/genomes/p')

for i,j in zip(['c', 'p'], ['modeling/testing_acc_c.json', 'modeling/testing_acc_p.json']):
    acc = json.load(open(j, 'r'))
    acc = acc[:3000]
    for a in acc:
        time.sleep(0.5)
        os.system('efetch -id '+a+' -db sequences -format fasta > testing/genomes/'+i+'/'+a+'.fasta')

