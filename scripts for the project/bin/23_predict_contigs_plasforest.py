#! python

import time
import json
import os
exec(open('scripts/lib/functions.py', 'r').read())

tool = 'PlasForest'
os.system('mkdir -p testing/benchmarking; rm -rf testing/benchmarking/%s; mkdir testing/benchmarking/%s' % (tool, tool))

dict1 = {}
for c in os.listdir('testing/simulated_contigs'):
    start = time.time()
    call('mkdir testing/benchmarking/%s/%s' % (tool, c))
    call('source activate plasforest; cd testing/benchmarking/%s/%s/; d=`pwd`; echo $d; cp ../../../simulated_contigs/%s /home/tianrm/software/PlasForest/%s.fasta; pushd /home/tianrm/software/PlasForest; python PlasForest.py -i %s.fasta -o $d/%s.csv -r --threads 8; popd' % (tool, c, c, c, c, c))
    end = time.time()

    dict1[c] = end - start

json.dump(dict1, open('testing/benchmarking/%s/time_used' % tool, 'w'))

