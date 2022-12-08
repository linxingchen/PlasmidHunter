#! python

import time
import json
import os

tool = 'PlasmidHunter'
os.system('mkdir -p testing/benchmarking; rm -rf testing/benchmarking/%s; mkdir testing/benchmarking/%s' % (tool, tool))

dict1 = {}
for c in os.listdir('testing/simulated_contigs'):
    start = time.time()
    os.system('python PlasmidHunter/PlasmidHunter_1.1/bin/PlasmidHunter.py -c 8 -i testing/simulated_contigs/%s -o testing/benchmarking/%s/%s' % (c, tool, c))
    end = time.time()

    dict1[c] = end - start

json.dump(dict1, open('testing/benchmarking/%s/time_used' % tool, 'w'))


