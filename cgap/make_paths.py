#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from config import FASTQ_PATH
from config import HITS_PATH
from config import HIT_FASTQ_PATH
from config import BLAST_PATH
from config import BAM_PATH
from config import VCF_PATH
from config import DEPTH_PATH
from config import CONSENSUS_FILES

def make_paths():
    directories = [FASTQ_PATH,
                   HITS_PATH,
                   HIT_FASTQ_PATH,
                   BLAST_PATH,
                   BAM_PATH,
                   VCF_PATH,
                   DEPTH_PATH,
                   CONSENSUS_FILES]
    for directory in directories:
        os.makedirs(directory)


def get_path(fasta_ref, fastq, directory, ext):
    fasta_name = os.basename(fasta_ref).rsplit(".")[0]
    fastq_name = os.basename(fastq).rsplit(".")[0]
    file_name = "{}.{}.{}".format(
        fasta_name,
        fastq_name,
        ext
    )
    path = os.path.join(directory, file_name)
    return path


def get_fasta_file_path(fasta_ref, fastq):
    path = get_path(fasta_ref, fastq, FASTA_PATH, ".hit")
    return path


def get_fastq_file_path(fasta_ref, fastq):
    path = get_path(fasta_ref, fastq, HIT_FASTQ_PATH, ".fastq")
    return path


def get_blast_file_path(fasta_ref, fastq):
    path = get_path(fasta_ref, fastq, BLAST_PATH, ".blast")
    return path


def get_bam_file_path(fasta_ref, fastq):
    path = get_path(fasta_ref, fastq, BAM_PATH, ".bam")
    return path


def get_vcf_file_path(fasta_ref, fastq):
    path = get_path(fasta_ref, fastq, VCF_PATH, ".vcf.gz")
    return path


def get_depth_file_path(fasta_ref, fastq):
    path = get_path(fasta_ref, fastq, DEPTH_PATH, ".tsv")
    return path


def get_cns_file_path(fasta_ref, fastq):
    path = get_path(fasta_ref, fastq, CONSENSUS_FILES, ".fa")
    return path


def get_blast_db_path(fastq):
