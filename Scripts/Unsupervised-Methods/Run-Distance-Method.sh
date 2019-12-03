#!/bin/bash

data=$1
version=$2
mode=$3
cutoff=$4

setDir=~/Lab/Target-Gene/Benchmark
train=$setDir/$data-Benchmark.$version.txt
outputDir=~/Lab/Target-Gene/Distance-Method/Results
enhancers=~/Lab/Target-Gene/Target-Finder/GM12878-Enhancers.bed
ccres=~/Lab/ENCODE/Encyclopedia/V4/Registry/V4-hg19/hg19-ccREs-Simple.bed
scriptDir=~/Projects/Target-Gene-Prediction/Scripts/Distance-Method
tss=~/Lab/Reference/Human/hg19/Gencode19/TSS.2019.bed
bedtools=~/bin/bedtools2/bin/bedtools
scriptDir=~/Projects/Target-Gene-Prediction/Scripts/Distance-Method
exp=~/Lab/Target-Gene/Benchmark/Characteristics/GM12878-TPM-Expression.txt

mkdir -p $outputDir


if [ $mode == "normal" ]
then
python $scriptDir/rank.distance.py $tss $ccres \
    $train $outputDir/$data-Distance.$version.txt
elif [ $mode == "expression" ]
then
python $scriptDir/rank.expression.distance.py $tss $ccres \
    $train $exp $cutoff $outputDir/$data-Distance-Expression.$cutoff.txt
fi
