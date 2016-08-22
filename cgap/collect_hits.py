#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from Bio import SeqIO

from .config import MIN_BLAST_SCORE

from .make_paths import get_blast_file_path
from .make_paths import get_fastq_file_path

def yield_hits(fasta_ref, fastq):
    ''' yields blast hits above a score from a tsv file '''
    blast_file = get_blast_file_path(fasta_ref, fastq)
    with open(blast_file) as input_handle:
        for line in input_handle:
            found = False
            columns = line.split()
            try:
                if float(columns[11]) >= MIN_BLAST_SCORE:
                    yield columns[1].strip()
            except IndexError:
                pass


def build_hits_collection(fasta_refs, fastq):
    ''' collects fastq hits from large fastq files '''
    hit_set = set()
    reference_hit_dict = {}

    for fasta_ref in fasta_refs:

        if fasta_ref not in reference_hit_dict:
            reference_hit_dict[fasta_ref] = set()

        hits = yield_hits(fasta_ref, fastq)

        for fqid in hits:

            if fqid not in hit_set:
                hit_set.add(fqid)

            reference_hit_dict[fasta_ref].add(fqid)

    return hit_set, reference_hit_dict


def get_fastq_hits(fastq, hit_set):
    ''' builds records collections '''
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
    ''' writes fastqs into smaller fastq files '''
    for fasta_ref in fasta_refs:
        fastq_path = get_fastq_file_path(fasta_ref, fastq)
        with open(fastq_path, "w+") as output_handle:
            for fqid in reference_hit_dict[fasta_ref]:
                SeqIO.write(hit_dict[fqid], output_handle, "fastq")
    return True

def collect_hits(fasta_refs, fastq):
    ''' runs the hits collection pipeline '''
    hit_set, reference_hit_dict = build_hits_collection(fasta_refs, fastq)
    hit_dict = get_fastq_hits(fastq, hit_set) #memory hog.
    write_fastqs(
        fasta_refs,
        fastq,
        reference_hit_dict,
        hit_dict
    )

def collect_hits_argslist(args):
    ''' runs hits collection pipeline with 1 argument '''
    if len(args) == 2:
        fastas, fastq = args
        collect_hits(fastas, fastq)
        return True
    return False
