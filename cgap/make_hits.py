#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import MIN_BLAST_SCORE
from make_paths import get_hits_file_path

def yield_hits(blast_file):
    with open(blast_file, "r") as input_handle:
        for line in input_handle:
            found = False
            columns = line.split()
            try:
                if float(columns[11]) >= MIN_BLAST_SCORE:
                    yield columns[1].strip()
            except IndexError:
                pass


def get_hits(fasta_ref, fastq):
    blast_file_path = get_blast_file_path(fasta_ref, fastq)
    hits_file_path = get_hits_file_path(fasta_ref, fastq)

    hit_gen = hit_generator(blast_file_path)

    with open(hits_file_path, "w+") as output_handle:
        for hit in hit_gen:
            output_handle.write("{}\n".format(hit)
    return True
