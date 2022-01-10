#!/bin/bash

#
# (c) 2021 Sven Lieber
# KBR Brussels
#
# This script extracts identified contributors with an identifier with a length bigger than 8
# These contributors do not have an authority records yet

if [ "$#" -ne 2 ];
then
  echo "use 'bash get-identified-authorities.sh <input csv file> <output csv file>"
  exit 1
fi

inputFile=$1
outputFile=$2

# write the CSV header
# apparently the header name 'contributorID' is also longer than 8, so it will be automatically copied too
# head -n 1 $inputFile > $outputFile

# extract contributors with an ID with more than 8 characters and append the found lines to the output file
awk -F, 'length($2) > 8 { print }' $inputFile >> $outputFile

