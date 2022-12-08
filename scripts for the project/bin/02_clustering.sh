cd database
#cd-hit -i proteins.faa -o clustered -c 0.7 -aL 0.9 -M 0 -T 100
mmseqs easy-linclust proteins.faa mmseqs tmp --min-seq-id 0.4 -c 0.8 --threads 100
