#!/bin/bash

kallisto quant -t 4 -b 100 \
-i mouse_index.idx \
--output-dir kallisto_out_$1 $2 $3