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
parse-vcf --vcf chr22.vcf.gz --out count_chr_22.csv --ind genetic_ids.txt
```

## Annotating SNPs
You can then annotate SNPs using a class inheriting from `Annotator` class. Several implementations are provided in the `snpbias.annotation` module.

We also provide a command line interface to annotate SNPs.

```bash
annotate-snp --input count_chr_22.csv --out annotated_freq_chr_22.csv --method freq
```
Where --method is one of:
- freq: Calculate the absolute difference in ratios of alt reads to total reads between a single pair of technologies
- chi2: Perform a Chi-squared test on the contingency table of alt and ref reads across multiple technologies
