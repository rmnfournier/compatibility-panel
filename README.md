# snp-bias
A Python package to annotate bias in ancient DNA data originating from sequencing platforms.

## Installation

You can start by creating a new environment:

```bash
conda create -n snp-bias python=3.11 
conda install conda-forge::pyvcf
```

You can then clone the current repository, and install the package:

```bash
pip install -e .
```

## Parsing the imputed VCF files
snp-bias provides an entry point to gather the read counts from VCF files that contain the read count information.

```bash
parse-vcf --vcf chr1.vcf.gz --out count_chr_1.csv --ind genetic_ids.txt
```

Alternatively, you can manually create the count files. The output file should be a CSV file with the following columns:
```csv
chr,pos,ref,alt,all_reads_AG,alt_reads_AG,all_reads_SG,alt_reads_SG
1,752566,G,A,65,35,744,372
1,776546,A,G,55,30,493,264
...
```
where 
all_reads_X is the total number of reads covering the SNP for technology X for individuals heterozygous at the SNP. 

## Annotating SNPs
You can then annotate SNPs using a class inheriting from `Annotator` class. Several implementations are provided in the `snpbias.annotation` module.

We also provide a command line interface to annotate SNPs.

```bash
annotate-snp --input count_chr_1.csv --out annotated_freq_chr_1.csv --method freq
```
Where --method is one of:
- freq: Calculate the absolute difference in ratios of alt reads to total reads between a single pair of technologies
- chi2: Perform a Chi-squared test on the contingency table of alt and ref reads across multiple technologies
- bayes: Perform a Bayesian analysis on the contingency table of alt and ref reads across multiple technologies

## Summarizing results
Finally, you can summarize the results and keep a certain quantile of SNPs with the best scores (which can be the highest or the lowest depending on the method used).

```bash
summarize-results --snp_file v64.snp --annotations annotated_freq_chr_@.txt --method freq --quantile 0.01 --out top_1_percent_snps.txt --out2 discarded_snps.txt
```
Where:
1. `--snp_file` a SNP file with 6 tab-separated columns: snp_name, chr, gen_map(optional, can be set to .), position, ref (optional, can be set to .), alt (optional, can be set to.)
2. `--annotations` is the annotated SNP file with '@' used as a placeholder in case the annotations are split across multiple files, 
3. `--method` is the method used for annotation,
4. `--quantile` is the quantile of SNPs to keep
5. `--out` is the output file for the top SNPs
6. `--out2` is an optional output file for the discarded SNPs.
