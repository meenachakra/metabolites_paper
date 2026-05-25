#!/bin/bash

module load STAR/2.7.11b

# 1st command line argument specifies a sample name
# 2nd and 3rd specify the trimmed paired end reads

STAR --genomeDir m37_GRCm39/ \
--readFilesIn $2 $3 \
--outFileNamePrefix ./$1 \
--outSAMunmapped Within \
--outSAMattributes NH HI AS NM MD XS \
--twopassMode Basic \
--alignSJDBoverhangMin 1 \
--alignSJoverhangMin 8 \
--runThreadN 16 \
--outSAMtype BAM SortedByCoordinate \
--outSAMstrandField intronMotif \
--readFilesCommand zcat