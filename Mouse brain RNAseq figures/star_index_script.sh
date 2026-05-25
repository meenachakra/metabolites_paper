#!/bin/bash

module load STAR/2.7.11b

# required files were downloaded from GENCODE
# https://www.gencodegenes.org/mouse/
# Release M37 (GRCm39)

STAR --runThreadN 16 \
--runMode genomeGenerate \
--genomeDir m37_GRCm39 \
--genomeFastaFiles GRCm39.primary_assembly.genome.fa \
--sjdbGTFfile gencode.vM37.primary_assembly.annotation.gtf \
--sjdbOverhang 149