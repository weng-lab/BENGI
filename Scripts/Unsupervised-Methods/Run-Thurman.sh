#!/bin/bash

data=$1
version=$2

setDir=~/Lab/Target-Gene/Benchmark
train=$setDir/$data-Benchmark.$version.txt
totalTrain=$setDir/$data-Benchmark.*.txt

scriptDir=~/Projects/Target-Gene-Prediction/Scripts/Correlation-Methods
featureDir=~/Lab/Target-Gene/Correlation-Methods/Thurman/Signal-Output
outputDir=~/Lab/Target-Gene/Correlation-Methods/Thurman/Results
signalDir=~/Lab/Target-Gene/Correlation-Methods/Thurman/Legacy-DNase
ccres=~/Lab/ENCODE/Encyclopedia/V4/Registry/V4-hg19/hg19-ccREs-Simple.bed
tss=~/Lab/Reference/Human/hg19/Gencode19/TSS.2019.bed 
mkdir -p $outputDir

######## Creating Enhancer Signal Matrix ################
if [ ! -f "$featureDir/$data-Enhancer-Matrix.txt" ]
then
    mkdir -p $featureDir/signal-output
    cd $featureDir/signal-output
    echo -e "Generating ELS signal matrix..."
    cat $totalTrain | awk '{print $1}' | sort -u > els
    awk 'FNR==NR {x[$1];next} ($5 in x)'  els $ccres | awk '{print $1 "\t" \
        $2 "\t" $3 "\t" $5}' | sort -u > els.bed
    list=$signalDir/Legacy-List.txt
    rm -f tmp1
    q=$(wc -l $list | awk '{print $1}')
    for j in `seq 1 1 $q`
    do
        echo $j
        file=$(awk '{if (NR == '$j') print $1}' $list)
        group=$(awk '{if (NR == '$j') print $3}' $list)
        ~/bin/bigWigAverageOverBed $signalDir/$file els.bed out1
        awk '{print "'$group'" "\t" $1 "\t" $5}' out1 >> tmp1
    done
    python $scriptDir/combine.biosamples.py tmp1 > \
        $featureDir/$data-Enhancer-Matrix.txt
    cd $featureDir
    rm -r $featureDir/signal-output
fi

######## Creating TSS Signal Matrix ################
if [ ! -f "$featureDir/$data-TSS-Matrix.txt" ]
then
    echo -e "Generating TSS signal matrix..."
    mkdir -p $featureDir/signal-output
    cd $featureDir/signal-output
    list=$signalDir/Legacy-List.txt

    cat $totalTrain | awk '{print $2}' | sort -u  > genes
    awk 'FNR==NR {x[$1];next} ($7 in x)' genes $tss > tss
    bedtools closest -t first -a tss -b $ccres | awk '{print $8 "\t" $9 "\t" \
        $10 "\t" $4}' > tss.bed
    list=$signalDir/Legacy-List.txt
    rm -f tmp1
    q=$(wc -l $list | awk '{print $1}')
    for j in `seq 1 1 $q`
    do
        echo $j
        file=$(awk '{if (NR == '$j') print $1}' $list)
        group=$(awk '{if (NR == '$j') print $3}' $list)
        ~/bin/bigWigAverageOverBed $signalDir/$file tss.bed out1
        awk '{print "'$group'" "\t" $1 "\t" $5}' out1 >> tmp1
    done
    python $scriptDir/combine.biosamples.py tmp1 > \
        $featureDir/$data-TSS-Matrix.txt
    cd $featureDir
    rm -r $featureDir/signal-output  
fi  

######## Running analysis ################

cd $outputDir

python $scriptDir/thurman.correlation.py $featureDir/$data-TSS-Matrix.txt \
    $featureDir/$data-Enhancer-Matrix.txt $tss $train > $outputDir/$data-Results.$version.txt
