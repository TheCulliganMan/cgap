#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgap

pipe_consensus(
        "Opn1mw.fa",
        "sm_test.1.fq",
        "sm_test.2.fq",
        'bamfile_working',
        'bamfile_final',
        'vcf_file_out',
        'depth_file',
        'cns_file'
    )
