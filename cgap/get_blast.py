#!/usr/bin/env python
import subprocess as sp

from .make_paths import get_blast_db_path
from .make_paths import get_blast_file_path


def run_blast(fasta_ref, fastq):
    """ Runs Blast on a local blast database """
    blast_db = get_blast_db_path(fastq)
    blast_file = get_blast_file_path(fasta_ref, fastq)

    cmd = ['blastall',
           '-p', 'blastn',
           '-d', blast_db,
           '-i', fasta_ref,
           '-v', '500000',
           '-m', '8']

    with open(blast_file, "w+") as output_handle:
        p1 = sp.Popen(cmd, stdout=output_handle)
        p1.communicate()
    return True


def run_blast_argslist(args):
    if len(args) == 2:
        fasta, fastq = args
        run_blast(fasta, fastq)
        return True
    return False
