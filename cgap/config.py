#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PROGRAM LOCATIONS
MARK_DUPLICATES_JAR_PATH = "/cGAP/bin/MarkDuplicates.jar"
SAMTOOLS_PATH = 'samtools'
BWA_PATH = 'bwa'
NOVOSORT_PATH = 'novosort'
TABIX_PATH = 'tabix'
BCFTOOLS_PATH = 'bcftools'

# QUALITY SETTINGS
## Minimum quality for bases to remain unmasked.
MASK_MIN_QUALITY = 20

## Minimum depth for bases to remain unmasked.
MASK_MIN_DEPTH = 4
