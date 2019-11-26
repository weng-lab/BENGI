## Scripts for generating benchmark datasets

### Generating Benchmark

```
./Generate-Benchmark.sh biosample linkType rawLinks name blackList
```

* *biosample* = name of the biosample from which we get the cCREs [GM12878, HeLa-S3, K562, ...]

* *linkType* = type of genomic interaction [ChIA-PET, Hi-C, CHi-C, eQTLs, CRISPR]

* *rawLinks* = path to raw data

* *name* = unique ID indicating biosample and link type [GM12878.RNAPII-ChIAPET, GM12878-HiC, ...]

* *blacklist* = should you blacklist ambiguous pairs [yes, no]

Example: to generate ELS-gene pairs using GM12878 RNAPII ChIA-PET data and removing ambiguous pairs
```
./Generate-Benchmark.sh GM12878 ChIA-PET GSM1872887_GM12878_RNAPII_PET_clusters.txt GM12878.RNAPII-ChIAPET yes
```
