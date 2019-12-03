#!/bin/bash

data=$1
version=$2
mode=$3

distance=~/Lab/Target-Gene/Distance-Method/Results/$data-Distance.$version.txt

correlation=~/Lab/Target-Gene/Correlation-Methods/Sheffield/Results/$data-Results.$version.txt

tf=~/Lab/Target-Gene/Target-Finder/Results-Full/$data-validation-*.$version.txt
#cat $tf


cd ~/Lab/Target-Gene/Distance-Method/Average-Rank

paste $distance $correlation | awk '{print $1 "\t" $2 "\t" $4}' | \
    sort -k2,2gr | awk 'BEGIN{x=0;r=0}{if (x != $2) r +=1; print $0 \
    "\t" r; x=$2}' | sort -k3,3gr | awk 'BEGIN{x=0;r=0}{if (x != $2) \
    r +=1; print $0 "\t" r "\t" ($NF+r)/2; x=$2}' | sort -k6,6g | \
    awk '{print $1 "\t" 1/$6 "\t" $2 "\t" $3 "\t" $4 "\t" $5 "\t" $6}' > tmp
     
mv tmp $data-Average-Rank.$version.txt
