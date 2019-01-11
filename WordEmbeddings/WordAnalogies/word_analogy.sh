#!/bin/sh

total_corr=0
total_count=0

# loop through each file in the input directory
for file in "$2"/*
do
    # output the current filename
    file_name=$(basename ${file})
    echo "$file_name"

    # call the python script and output the accuracy
    line_count="$(cat ${file} | wc -l)"
    acc_count="$(python3 word_analogy.py "$1" "$file" "$3"/"$file_name" "$4" "$5")"
    acc_perc=$(echo "($acc_count/$line_count)*100" | bc -l)
    echo "ACCURACY TOP1: ${acc_perc}%"

    # increment the counts for total accuracy
    total_corr=$(echo "$total_corr+$acc_count" | bc -l)
    total_count=$(echo "$total_count+$line_count" | bc -l)
done

# output the total accuracy
total_perc=$(echo "($total_corr/$total_count)*100" | bc -l)
echo "Total accuracy: ${total_perc}%"