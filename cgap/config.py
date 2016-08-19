#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import abspath

CORES = int(6)

# WORK LOCATIONS
FASTA_FILES = abspath("fasta_files")
HITS_PATH = abspath("hit_files")
HIT_FASTQ_PATH = abspath("hit_fastq_files")
BLAST_PATH = abspath('blast_files')
BAM_PATH = abspath('bam_files')
VCF_PATH = abspath('vcf_files')
DEPTH_PATH = abspath('depth_files')
CONSENSUS_FILES = abspath('consensus_files')

# PROGRAM LOCATIONS
MARK_DUPLICATES_JAR_PATH = "/cGAP/bin/MarkDuplicates.jar"
SAMTOOLS_PATH = 'samtools'
BWA_PATH = 'bwa'
NOVOSORT_PATH = 'novosort'
TABIX_PATH = 'tabix'
BCFTOOLS_PATH = 'bcftools'

# QUALITY SETTINGS
## Minimum quality for bases to remain unmasked.
## Integers only!!!
MASK_MIN_QUALITY = int(20)

## Minimum depth for bases to remain unmasked.
## Integers only!!!
MASK_MIN_DEPTH = int(4)

## Minimum Blast Score
MIN_BLAST_SCORE = float(50.0)
