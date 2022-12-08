#! python

from BCBio import GFF
import json
import os
from multiprocessing import Pool
import pandas as pd

def gff_to_dict(gff):
    dict1 = {}
    print(gff)
    for rec in GFF.parse(gff):
        dict1[rec.id] = {}
        dict1[rec.id]['size'] = rec.features[0].location.end - rec.features[0].location.start
        dict1[rec.id]['loc'] = rec.features[0].qualifiers['genome'][0]
        dict1[rec.id]['protein_id'] = [rec.features[i].sub_features[0].qualifiers['Name'][0] for i in range(1,len(rec.features)) if rec.features[i].sub_features and rec.features[i].sub_features[0].qualifiers.get('Name')]

    return(dict1)

def try_gff_to_dict(gff):
    try:
        return(gff_to_dict(gff))
    except:
        return(None)

dict1 = {}
pool = Pool(150)
out = [pool.apply_async(try_gff_to_dict, ('modeling/gff/'+f,)) for f in os.listdir('modeling/gff')] 
pool.close()
pool.join()

out2 = [i.get() for i in out]
out2 = [i for i in out2 if i != None]
for i in out2:
    dict1.update(i)

# summary
dict2 = {i:{'loc':dict1[i]['loc'],'size':dict1[i]['size']} for i in dict1}
df = pd.DataFrame.from_dict(dict2).transpose()
c = df.loc[(df['loc'] == 'chromosome') & ((df['size'] > 900000)),:]
p = df.loc[(df['loc'] == 'plasmid') & ((df['size'] < 600000)),:]
df.loc[p.index,'class'] = 'plasmid'
df.loc[c.index,'class'] = 'chromosome'
df['class'].fillna('unsure', inplace=True)
df['count'] = 1
df1 = df.groupby(['loc', 'class']).sum()
df1.to_csv('modeling/summary.txt', sep='\t')

# save amplicons with confirmed type (chromosome or plasmid)
dict3 = {i:dict1[i] for i in df.loc[df['class']!='unsure',:].index}
json.dump(dict3, open('modeling/gff.json', 'w'))
