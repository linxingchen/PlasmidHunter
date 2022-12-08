mkdir -p gcp_vs_kmer
cd gcp_vs_kmer
rm -rf genbank
for i in {GCA_000008865.2,GCA_019738995.1,GCA_009363835.1}; do ncbi-genome-download -A $i -s genbank -F fasta all; gzip -d genbank/bacteria/$i/$i*.gz; done
cd ..
