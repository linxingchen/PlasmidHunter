#! python

import pandas as pd
import os
from multiprocessing import Pool

df = pd.read_csv('scripts/lib/prokaryotes.csv', header = 0, index_col = 0)

os.system('mkdir -p modeling; rm -rf modeling/gff; mkdir modeling/gff')
os.chdir('modeling/gff')

def download(url):
    os.system('wget '+url+'/'+url.split('/')[-1]+'_genomic.gff.gz')

pool = Pool(50)
for i in df['RefSeq FTP']:
    pool.apply_async(download, (i,))

pool.close()
pool.join()

os.system('gzip -d *')
os.chdir('../../')
