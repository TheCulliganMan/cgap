#!/usr/bin/env python
import os

def get_fasta_names(fasta_paths):
    for fasta_path in fasta_paths:
        fasta_name = basename(path).split('.')[0]
        yield fasta_name

def get_fasta_paths(fasta_dir):
    fa_ext = ('.fa', '.fasta', '.fna')
    for fasta in os.listdir(fasta_dir):
        if not fasta.endswith(fa_ext):
            continue
        rel_path = os.path.join(fasta_dir, fasta)
        abs_path = os.path.abspath(rel_path)
        yield abs_path

def bwa_index_fasta(fasta_path):
    cmd = ['bwa', 'index', file_path]
    return sp.call(cmd)

def samtools_index_fasta(fasta_path):
    cmd = ['samtools', 'faidx', fasta_path]
    return sp.call(cmd)

def index_fasta(fasta_path):
    statuses = []
    statuses.append(bwa_index_fasta(fasta_path))
    statuses.append(samtools_index_fasta(fasta_path))
    return statuses
