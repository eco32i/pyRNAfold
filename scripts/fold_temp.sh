#!/bin/bash

# Runs RNAfold for the given RNA sequence over the range of temperatures,
# extracts base pairing probabilities and saves them in .txt files 
# for later analysis

# FASTA file with RNA sequence
psext="_dp.ps"
rna_fa=${1:-rna.fa}

# Temperature interval limits
T1=${2:-37}
T2=${3:-43}

if [[ ! -f $rna_fa ]]
then
    echo "Could not find $rna_fa ... Exiting."
    exit 1
fi

# Get the base_name either from the fasta file or the filename
base_name=`awk '/^>/' $rna_fa | head -1`
if [[ -z "$base_name" ]]
then
    base_name="${rna_fa%.*}"
else
    base_name=${base_name##>}
fi
# Iterate over the T range and save probabilities to .txt file
for T in $(seq $T1 $T2)
do
    echo "Running RNAfold for Temp=$T ..."
    RNAfold -p -d2 --noPS --noLP -T $T < $rna_fa
    tmpf=`ls | grep _dp.ps`
    grep "^[0-9].*ubox$" $tmpf > ${base_name}_${T}.txt
done
rm ${base_name}_dp.ps
