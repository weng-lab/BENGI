#!/bin/bash
#SBATCH --nodes 1
#SBATCH --time=60:00:00
#SBATCH --mem=10G
#SBATCH --output=/home/moorej3/Job-Logs/jobid_%A.output
#SBATCH --error=/home/moorej3/Job-Logs/jobid_%A.error
#SBATCH --partition=5days

data=GM12878.RNAPII-ChIAPET
version=v3

biosample=$(echo $data | awk -F "." '{print $1}')

echo $data
setDir=~/Lab/Target-Gene/Benchmark
train=$setDir/$data-Benchmark.$version.txt
totalTrain=$setDir/$data-Benchmark.*.txt
peakDir=~/Lab/Target-Gene/Target-Finder/Original-Code/targetfinder/$biosample/peaks
featureDir=~/Lab/Target-Gene/Target-Finder/Feature-Matrices
outputDir=~/Lab/Target-Gene/Target-Finder/Results-Full
ccres=~/Lab/ENCODE/Encyclopedia/V4/Registry/V4-hg19/hg19-ccREs-Simple.bed
scriptDir=~/Projects/Target-Gene-Prediction/Scripts/TargetFinder
tss=~/Lab/Reference/Human/hg19/Gencode19/TSS.2019.bed
bedtools=~/bin/bedtools2/bin/bedtools

mkdir -p /tmp/moorej3/$SLURM_JOBID
cd /tmp/moorej3/$SLURM_JOBID

mkdir -p $outputDir

ls $peakDir/* | grep -v csv | awk -F "/" '{print $NF}' > peak-list.txt
num=$(wc -l peak-list.txt | awk '{print $1}')


######## Creating Enhancer Feature Matrix ################
if [ ! -f "$featureDir/$data-Enhancer-Feature-Matrix.txt" ]
then
    echo -e "Generating enhancer feature matrix..."
    cat $totalTrain | awk '{print $1}' | sort -u  > cres
    awk 'FNR==NR {x[$1];next} ($5 in x)' cres $ccres | \
    awk '{print $1 "\t" $2 "\t" $3 "\t" $5 "\t" $6}' > enhancers
    for k in $(seq $num)
    do
        echo $k
        peakFile=$(cat peak-list.txt | awk -F "\t" '{if (NR == '$k') print $1}')
        if [[ $peakFile =~ "Cage" ]]
        then
            mode="cage"
        elif [[ $peakFile =~ "Rrbs" ]]
        then
            mode="rrbs"
        else
            mode="peaks"
        fi
        $bedtools intersect -wo -a enhancers -b $peakDir/$peakFile > tmp
        head -n 1 tmp | column -t
        python $scriptDir/process.overlaps.py enhancers tmp $mode | sort -k1,1 | \
            awk 'BEGIN {print "cREs" "\t" "'$peakFile'"}{print $0}'> col.$k
    done
    paste col.* | awk '{printf "%s\t", $1; for(i=2;i<=NF;i+=2) printf "%s\t", \
        $i;print ""}' > $featureDir/$data-Enhancer-Feature-Matrix.txt
    rm col.*
fi

######## Creating TSS Feature Matrix ################
if [ ! -f "$featureDir/$data-TSS-Feature-Matrix.txt" ]
then
    echo -e "Generating tss feature matrix..."
    cat $totalTrain | awk '{print $2}' | sort -u  > genes
    awk 'FNR==NR {x[$1];next} ($7 in x)' genes $tss | \
        awk '{print $1 "\t" $2-500 "\t" $3+500 "\t" $4 "\t" $7 }' > tss
    for k in $(seq $num)
    do
        echo $k
        peakFile=$(cat peak-list.txt | awk -F "\t" '{if (NR == '$k') print $1}')
        if [[ $peakFile =~ "Cage" ]]
        then
            mode="cage"
        elif [[ $peakFile =~ "Rrbs" ]]
        then
            mode="rrbs"
        else
            mode="peaks"
        fi
        $bedtools intersect -wo -a tss -b $peakDir/$peakFile > tmp
        python $scriptDir/process.overlaps.py tss tmp $mode | sort -k1,1 | \
            awk 'BEGIN {print "cREs" "\t" "'$peakFile'"}{print $0}'> col.$k
    done
    paste col.* | awk '{printf "%s\t", $1; for(i=2;i<=NF;i+=2) printf "%s\t",\
        $i;print ""}' > $featureDir/$data-TSS-Feature-Matrix.txt
    rm col.*
fi

######## Creating Window Matrix ################
if [ ! -f "$featureDir/$data-Window-Feature-Matrix.txt" ]
then
    echo -e "Generating window feature matrix..."
    cat $totalTrain | awk '{print $1 "\t" $2}' | sort -u > pairs
    awk 'FNR==NR {x[$1];next} ($5 in x)' pairs $ccres | \
        awk '{print $1 "\t" $2 "\t" $3 "\t" $5 "\t" $6 }' > enhancers
    python $scriptDir/create.window.py $tss enhancers pairs > windows

    for k in $(seq $num)
    do
        echo $k
        peakFile=$(cat peak-list.txt | awk -F "\t" '{if (NR == '$k') print $1}')
        if [[ $peakFile =~ "Cage" ]]
        then
            mode="cage"
        elif [[ $peakFile =~ "Rrbs" ]]
        then
            mode="rrbs"
        else
            mode="peaks"
        fi
        $bedtools intersect -wo -a windows -b $peakDir/$peakFile > tmp
        python $scriptDir/process.overlaps.py windows tmp $mode | sort -k1,1 | \
            awk 'BEGIN {print "cREs" "\t" "'$peakFile'"}{print $0}'> col.$k
    done
    paste col.* | awk '{printf "%s\t", $1; for(i=2;i<=NF;i+=2) printf "%s\t",\
        $i;print ""}' > $featureDir/$data-Window-Feature-Matrix.txt
    rm col.*
fi

######## Creating Distance Matrix ################
if [ ! -f "$featureDir/$data-Distance.txt" ]
then
    echo -e "Generating distance matrix..."
    awk '{print $1 "\t" $2}' $totalTrain | sort -u > pairs
    python $scriptDir/calculate.distance.py $tss $enhancers pairs > \
        $featureDir/$data-Distance.txt 
fi


######## Running Random Forest/GBM ################
echo -e "Running Model..."
cat $totalTrain | awk '{print $2}' | sort -u  > genes
awk 'FNR==NR {x[$1];next} ($7 in x)' genes $tss | \
awk '{print $1 "\t" $2-500 "\t" $3+500 "\t" $4 "\t" $7 }' > tss

python $scriptDir/gradient.boosting.v2.py $train $featureDir/$data-Enhancer-Feature-Matrix.txt \
    $featureDir/$data-TSS-Feature-Matrix.txt $featureDir/$data-Window-Feature-Matrix.txt \
    tss $data $outputDir $version

rm -r /tmp/moorej3/$SLURM_JOBID
