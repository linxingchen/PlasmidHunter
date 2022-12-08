#! python

import pandas as pd
import os
from multiprocessing import Pool

df = pd.read_csv('scripts/lib/prokaryotes.csv', header = 0, index_col = 0)

os.chdir('database')
os.system('rm -rf proteins; mkdir proteins')
os.chdir('proteins')

def download(url):
    os.system('wget '+url+'/'+url.split('/')[-1]+'_protein.faa.gz')

pool = Pool(20)
for i in df['RefSeq FTP']:
    pool.apply_async(download, (i,))

pool.close()
pool.join()

os.system('pigz -d *gz; cat *faa > ../proteins.faa')
os.chdir('../../')
