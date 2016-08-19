#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgap

#cgap.make_paths()

fastqs = ['sm_test.1.fq','sm_test.2.fq']
fasta_ref = 'Opn1mw.fa'

for fastq in fastqs:
    pass
    #cgap.run_format_cmd(fastq)
    #cgap.run_blast(fasta_ref, fastq)
    cgap.collect_hits([fasta_ref], fastq)
