#!/bin/bash

module load rmats-turbo/4.1.1
module load cmake/3.14.0

rmats.py --gtf gencode.v47.primary_assembly.annotation.gtf \
--b1 vehicle_bam.txt --b2 treated_bam.txt --od rmats_turbo \
--tmp rmats_tmp \
-t paired --libType fr-unstranded \
--readLength 150 --variable-read-length \
--nthread 10 --cstat 0.1 --novelSS --allow-clipping