#!/bin/bash

trim_galore -q 30 \
--fastqc --stringency 3 --max_n 15 --output_dir trimming_out \
--cores 2 --retain_unpaired \
--paired ${1}_1.fq.gz ${1}_2.fq.gz