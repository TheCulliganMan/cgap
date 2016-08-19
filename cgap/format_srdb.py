#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess as sp

from Bio import SeqIO

def fastq_to_fasta(fastq_path):
    with open(fastq_path) as input_handle:
        for record in SeqIO.parse(input_handle, 'fastq'):
            yield record.format('fasta')


def run_format_cmd(fastq_path):
    format_cmd = ['formatdb',
                  '-i', 'stdin',
                  '-n', fastq_path,
                  '-p', 'F']

    p1 = Popen(
        format_cmd,
        stdin=subprocess.PIPE
    )

    fasta_generator = fastq_to_fasta(fastq_path)

    for fasta_record in fasta_generator:
        p1.stdin.write(fasta_record)

    return True
