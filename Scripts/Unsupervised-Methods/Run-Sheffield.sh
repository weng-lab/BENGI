#!/bin/bash

data=$1
version=$2
biosample=$(echo $data | awk -F "." '{print $1}')

echo $biosample

setDir=~/Lab/Target-Gene/Benchmark
train=$setDir/$data-Benchmark.$version.txt

scriptDir=~/Projects/Target-Gene-Prediction/Scripts/Correlation-Methods
featureDir=~/Lab/Target-Gene/Correlation-Methods/Sheffield/Signal-Matrices
outputDir=~/Lab/Target-Gene/Correlation-Methods/Sheffield/Results


signalDir=~/Lab/Target-Gene/Correlation-Methods/Sheffield/
stats=$featureDir/gene-summary.txt
ccres=~/Lab/ENCODE/Encyclopedia/V4/Registry/V4-hg19/hg19-ccREs-Simple.bed
genes=~/Lab/Reference/Human/hg19/Gencode19/Genes.bed
mkdir -p $outputDir


awk 'FNR==NR {x[$1];next} ($5 in x)'  $train $ccres | awk '{print $1 "\t" \
        $2 "\t" $3 "\t" $5}' | sort -u > els.bed
bedtools intersect -wo -a els.bed -b $featureDir/DHS.bed > enhancer-matrix.txt
        
cat $train | awk '{print $2}' | sort -u  > genes
awk 'FNR==NR {x[$1];next} ($4 in x)' genes $genes > genesFull

python $scriptDir/sheffield.correlation.py $featureDir/Exp.bed genesFull \
    enhancer-matrix.txt $stats $train $biosample > $outputDir/$data-Results.$version.txt
