#!/bin/bash

module load STAR/2.7.11b

# required files were downloaded from GENCODE
# https://www.gencodegenes.org/human/

STAR --runMode genomeGenerate \
     --genomeDir star_index \
     --genomeFastaFiles GRCh38.primary_assembly.genome.fa \
     --sjdbGTFfile gencode.v47.primary_assembly.annotation.gtf \
     --sjdbOverhang 149 \
     --runThreadN 16