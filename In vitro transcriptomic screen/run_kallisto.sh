#!/bin/bash

kallisto quant -t 4 -b 100 \
-i kallisto_index/Homo_sapiens.GRCh38.cdna.all.release-110_k31.idx \
--output-dir kallisto_out_$1 $2 $3