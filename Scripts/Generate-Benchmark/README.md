## Scripts for generating benchmark datasets

### Generating Benchmark

```
./Generate-Benchmark.sh biosample linkType rawLinks name blackList
```

* *biosample* = [GM12878, HeLa-S3, K562, ...]

* *lineType* = [ChIA-PET, Hi-C, CHi-C, eQTLs, CRISPR]

* *rawLinks* = path to raw data

* *name* = [GM12878.RNAPII-ChIAPET, GM12878-HiC, ...]

* *blacklist* = [yes, no]

Example:
```
./Generate-Benchmark.sh GM12878 ChIA-PET GSM1872887_GM12878_RNAPII_PET_clusters.txt GM12878.RNAPII-ChIAPET yes
```
