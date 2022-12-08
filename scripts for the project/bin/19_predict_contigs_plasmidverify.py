#! python

import time
import json
import os
exec(open('scripts/lib/functions.py', 'r').read())

tool = 'PlasmidVerify'
os.system('mkdir -p testing/benchmarking; rm -rf testing/benchmarking/%s; mkdir testing/benchmarking/%s' % (tool, tool))

dict1 = {}
for c in os.listdir('testing/simulated_contigs'):
    start = time.time()
    call('mkdir testing/benchmarking/%s/%s' % (tool, c))
    call('python ~/software/plasmidVerify/plasmidverify.py -f testing/simulated_contigs/%s -o testing/benchmarking/%s/%s --hmm /media/Data_1/tianrm/databases/Pfam-A.hmm -t 8' % (c, tool, c))
    end = time.time()

    dict1[c] = end - start

json.dump(dict1, open('testing/benchmarking/%s/time_used' % tool, 'w'))

