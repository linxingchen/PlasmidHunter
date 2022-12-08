#! python

import time
import json
import os
exec(open('scripts/lib/functions.py', 'r').read())

tool = 'Deeplasmid'
os.system('mkdir -p testing/benchmarking; rm -rf testing/benchmarking/%s; mkdir testing/benchmarking/%s' % (tool, tool))

dict1 = {}
for c in os.listdir('testing/simulated_contigs'):
    start = time.time()
    call('mkdir testing/benchmarking/%s/%s' % (tool, c))
    call('docker run -it -v /media/Data_1/tianrm/projects/plasmid_identification/3/testing/simulated_contigs/%s:/srv/jgi-ml/classifier/dl/in.fasta -v /media/Data_1/tianrm/projects/plasmid_identification/3/testing/benchmarking/%s/%s:/srv/jgi-ml/classifier/dl/outdir billandreo/deeplasmid-cpu-ubuntu  feature_DL_plasmid_predict.sh in.fasta outdir' % (c, tool, c))
    end = time.time()

    dict1[c] = end - start

json.dump(dict1, open('testing/benchmarking/%s/time_used' % tool, 'w'))

