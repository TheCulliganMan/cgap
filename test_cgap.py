#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgap

fastqs = ['sm_test.1.fq','sm_test.2.fq']
fastas = ['Opn1mw.fa']

# Setup for cgap run
cgap.make_paths()

# Create small fastqs
for fastq in fastqs:
    cgap.run_format_cmd(fastq)
    for fasta in fastas:
        cgap.run_blast(fasta, fastq)
    cgap.collect_hits([fasta], fastq)

# generate consensus
cgap.pipe_consensus(fastas[0], fastqs[0], fastqs[1])
