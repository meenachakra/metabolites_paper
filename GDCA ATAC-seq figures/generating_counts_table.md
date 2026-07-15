# Peak calling and IDR

Much of this code was based on the process described here:
https://pubmed.ncbi.nlm.nih.gov/33606259/

## Called peaks for the individual replicates from each brain

The following command was run - using MACS2 version 2.1.1 - for each of the 16 replicates (two replicates per brain, each representing an independent set of nuclei).

```
macs2 callpeak -t <replicate_name>.bam -n <replicate_name>.MACS2 -g mm -f BAMPE --to-large -p 1e-1 --keep-dup all --nomodel
```

## Merged BAM files for the individual replicates from each brain

The following command was run for each of the brains.

```
samtools merge <brain_name>.pooled.bam <brain_rep1>.bam <brain_rep2>.bam 
```

## Called peaks for the pooled dataset for each brain

Used the following MACS2 command (again using version 2.1.1):

```
macs2 callpeak -t <brain_name>.pooled.bam -n <brain_name>.pooled.MACS2 -g mm -f BAMPE --to-large -p 1e-1 --keep-dup all --nomodel
```

## Sorted the pooled BAM files and generated pseudoreplicates

For sorting, the following command was run for each of the brains.

```
samtools sort -o <brain_name>.pooled.sorted.bam <brain_name>.pooled.bam --threads 4
```

[Note that the pooled bam files above were actually already sorted based on samtools stats;
sorted explicitly just in case, based on the article.]

To generate pseudoreplicates:
- The script BAMPseudoReps.py from the Github repository https://github.com/georgimarinov/GeorgiScripts was converted to Python 3 using the program 2to3. The conversion was executed using Python 3.10.
- On July 9, 2025, the following file was downloaded and unzipped: https://hgdownload.soe.ucsc.edu/goldenPath/mm10/bigZips/mm10.fa.gz
- The following command was run for each brain.

```
python BAMPseudoReps.py <brain_name>.pooled.sorted.bam samtools mm10.fa
```

## Called peaks for the pseudoreplicates of each pooled dataset

Used the following MACS2 commands (again using version 2.1.1):

```
macs2 callpeak -t <brain_name>.pooled.sorted.pseudoRep1.bam -n <brain_name>.pooled.sorted.pseudoRep1.MACS2 -g mm -f BAMPE --to-large -p 1e-1 --keep-dup all --nomodel

macs2 callpeak -t <brain_name>.pooled.sorted.pseudoRep2.bam -n <brain_name>.pooled.sorted.pseudoRep2.MACS2 -g mm -f BAMPE --to-large -p 1e-1 --keep-dup all --nomodel
```

## Retained the top 300,000 peaks from each peak call set

Above, we generated 16 + 8 + 16 = 40 peak call sets (including narrowPeak files). We then wanted to retain 300,000 top peaks from each peak call set, using the MACS2 p-value as the ranking measure.

As per the following link, -log10(p-value) is the 8th column of a narrowPeak file: https://hbctraining.github.io/Intro-to-ChIPseq/lessons/05_peak_calling_macs.html

Higher values are more significant, so we sorted each narrowPeak file and took the top 300,000 as follows:

```
cat <narrowpeak_file> | sort --parallel=4 -k 8nr,8nr | awk 'BEGIN{OFS="\t"}{$4="Peak_"NR ; print $0}' | head -300000 | pigz -p 4 -c > <narrowpeak_file>.sorted.300K.gz
```

## Ran IDR on individual replicates to derive Nt for each brain

An IDR environment was created as follows.

```
mamba create -n idr_env -c bioconda -c conda-forge idr=2.0.4.2
```

Within that environment, the following command was run for each brain:

```
idr --samples <rep1_narrowpeak>.sorted.300K.gz <rep2_narrowpeak>.sorted.300K.gz --input-file-type narrowPeak --output-file <brain_name>.indRep.IDR --peak-list <brain_narrowpeak>.sorted.300K.gz --rank p.value --soft-idr-threshold 0.05 --plot
```

Nt was reported in the output of the command, as the "Number of peaks passing IDR cutoff of 0.05"

## Ran IDR on pooled pseudoreplicates to derive Np for each brain

Again within the IDR environment, ran the following command for each brain:

```
idr --samples <brain_pseudorep1_narrowpeak>.sorted.300K.gz <brain_pseudorep2_narrowpeak>.sorted.300K.gz --input-file-type narrowPeak --output-file <brain_name>.pooled.pseudorep.IDR --peak-list <brain_narrowpeak>.sorted.300K.gz --rank p.value --soft-idr-threshold 0.05 --plot
```

Np was reported in the output of the command, as the "Number of peaks passing IDR cutoff of 0.05"

## For each brain, selected the top max(Nt, Np) peaks from the pooled dataset peak calls

Ran the following command for each brain:

```
zcat <brain_narrowpeak>.sorted.300K.gz | head -n max_ntnp > <brain_name>.IDR0.05.bed
```

# Merging peaks across brain samples

The main workhorse for this step was the createIterativeOverlapPeakSet.R script downloaded from https://github.com/corceslab/ATAC_IterativeOverlapPeakMerging in July 2025.

The script requires MACS2 summit files, so the first step was:

## Filtered MACS2 summit files for each brain to only the peaks included in the IDR 0.05 bed file

A mapping from original peak names to the peak names in the IDR 0.05 file was determined as follows:

```
cat <brain_narrowpeak_file> | \
sort --parallel=4 -k 8nr,8nr | \
awk '{print $4, "Peak_"NR}' | \
head -300000 > <brain_narrowpeak_file>.name_mapping.tsv
```

Then this name mapping was used to filter the MACS2 summit files for each brain, using the IDR 0.05 bed file for each brain.

The filtered summit files are in the for_merging_peaks subfolder of this folder.

## Created the environment needed to run the merging script

The specifications of the created conda environment are contained within this folder, within the file: peak_merge_atac_env.yml

The relevant BSGenome package was also downloaded as follows:

```
Rscript -e 'if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager", repos = "https://cran.rstudio.com")'

Rscript -e 'BiocManager::install("BSgenome.Mmusculus.UCSC.mm10")'
```

## Made the necessary metadata file

This metadata file is contained within this folder, as iterative_overlap_metadata.txt

## Downloaded the necessary mm10 blacklist file

Downloaded from the following link:

https://github.com/Boyle-Lab/Blacklist/tree/master/lists

File: mm10-blacklist.v2.bed.gz

Downloaded on July 11, 2025

## Ran the merging script with the conda environment

Command executed:

```
Rscript createIterativeOverlapPeakSet.R \
--metadata iterative_overlap_metadata.txt \
--macs2dir for_merging_peaks/ \
--outdir merged_peaks/ --suffix _summits.bed \
--blacklist mm10-blacklist.v2.bed \
--genome mm10 --spm 0 --rule "(n+1)/2" --extend 250
```

The output is contained within the merged_peaks subfolder of this folder.

# Generating a counts table

## Converted bed file from the merging script to saf

Script used: bed_to_saf_updated.py in the merged_peaks subfolder of this folder.

Explanation of script:

BED format uses a 0-based, half-open coordinate system (Source: https://samtools.github.io/hts-specs/BEDv1.pdf)

For SAF (used for featureCounts, below), the start and end positions are inclusive, see source here:
https://bioconductor.org/packages/release/bioc/vignettes/Rsubread/inst/doc/SubreadUsersGuide.pdf

Based on the description in the user guide, SAF should follow the same coordinate system as GTF, which is 1-based (source: https://useast.ensembl.org/info/website/upload/gff.html?)

Also see this forum:
https://www.biostars.org/p/228636/

So in the script, 1 is added to the start position whereas the end position remains untouched.

Output: All_Samples.fwp.filter.non_overlapping.saf within the merged_peaks subfolder of this folder

## Ran featureCounts as follows

Version: 2.0.6

```
featureCounts -p --countReadPairs -B -C -T 8 -F SAF -a All_Samples.fwp.filter.non_overlapping.saf -o All_Samples.counts Brain_1_pooled.sorted.bam Brain_2_pooled.sorted.bam Brain_3_pooled.sorted.bam Brain_4_pooled.sorted.bam Brain_5_pooled.sorted.bam Brain_6_pooled.sorted.bam Brain_7_pooled.sorted.bam Brain_8_pooled.sorted.bam
```

The output file, All_Samples.counts, is contained in this folder.