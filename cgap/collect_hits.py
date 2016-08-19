#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from Bio import SeqIO

from config import HITS_PATH
from make_paths import get_hits_file_path
from make_paths import get_hit_fastq_path

def hits_generator(hits_file_path):
    hit_set = set()
    with open(hits_file_path) as input_handle:
        for line in input_handle:
            yield line.split()


def build_hits_collection(fasta_refs, fastq):
    hit_set = set()
    reference_hit_dict = {}

    for fasta_ref in fasta_refs:

        if fasta_ref not in reference_hit_dict:
            reference_hit_dict[fasta_ref] = set()

        hits_path = get_hits_file_path(fasta_ref, fastq)
        hits = hits_generator(hits_path)

        for fqid in hits:

            if fqid not in hit_set:
                hit_set.add(fqid)

            reference_hit_dict[fasta_ref].add(fqid)

    return hit_set, reference_hit_dict


def get_fastq_hits(fastq, hit_set):
    hit_dict = {}
    with open(fastq) as input_handle:
        for record in SeqIO.parse(input_handle, 'fastq'):
            if record.id in hit_set:
                hit_dict[record.id] = record
    return hit_dict


def write_fastqs(
        fasta_refs,
        fastq,
        reference_hit_dict,
        hit_dict):
    for fasta_ref in fasta_refs:
        fastq_path = get_hits_fastq_path(fasta_ref, fastq)
        with open(fastq_path, "w+") as output_handle:
            for fqid in reference_hit_dict[fasta_ref]:
                SeqIO.write(hit_dict[fqid], output_handle, "fastq")
    return True

def collect_hits(fasta_refs, fastq):
    hit_set, reference_hit_dict = build_hits_collection(fasta_refs, fastq)
    hit_dict = get_fastq_hits(fastq, hit_set) #memory hog.
    write_fastqs(
        fasta_refs,
        fastq,
        reference_hit_dict,
        hit_dict
    )
