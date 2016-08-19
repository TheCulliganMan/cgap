#!/usr/bin/env python
import subprocess as sp

from .make_paths import get_blast_file_path
from .make_paths import get_blast_db_path

def run_blast(fasta_ref, fastq):

    blast_db = get_blast_db_path(fastq)
    blast_file = get_blast_file_path(fasta_ref, fastq)

    cmd = ['blastall',
           '-p', 'blastn',
           '-d', blast_db,
           '-i', fasta_ref,
           '-v', '500000',
           '-m', '8']

    with open(blast_file, "w+") as output_handle:
        status = sp.call(cmd, stdout=output_handle)

    return status
