#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import abspath

CORES = int(6)

# WORK LOCATIONS
##Created in your current working directory
FASTQ_PATH = abspath("fastq_files")
HITS_PATH = abspath("hit_files")
HIT_FASTQ_PATH = abspath("hit_fastq_files")
BLAST_PATH = abspath('blast_files')
BAM_PATH = abspath('bam_files')
VCF_PATH = abspath('vcf_files')
DEPTH_PATH = abspath('depth_files')
CONSENSUS_FILES = abspath('consensus_files')
PHYLIP_FILES = abspath('phylip_files')
CODEML_PHYLIP_FILES = abspath('codeml_phylip_files')
NEXUS_FILES = abspath('nexus_files')

# PROGRAM LOCATIONS
MARK_DUPLICATES_JAR_PATH = "/bin/MarkDuplicates.jar"
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

## Minimum Blast Score #we used 50.0
MIN_BLAST_SCORE = float(50.0)
