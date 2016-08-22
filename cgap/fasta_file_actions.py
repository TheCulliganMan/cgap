#!/usr/bin/env python
import os

def get_fasta_paths(fasta_dir):
    ''' Returns the absolute path of a fasta reference '''
    fa_ext = ('.fa', '.fasta', '.fna')
    for fasta in os.listdir(fasta_dir):
        if not fasta.endswith(fa_ext):
            continue
        rel_path = os.path.join(fasta_dir, fasta)
        abs_path = os.path.abspath(rel_path)
        yield abs_path
