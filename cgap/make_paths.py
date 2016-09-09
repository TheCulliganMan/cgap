#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from .config import BAM_PATH
from .config import BLAST_PATH
from .config import CONSENSUS_FILES
from .config import DEPTH_PATH
from .config import FASTQ_PATH
from .config import PHYLIP_FILES
from .config import CODEML_PHYLIP_FILES
from .config import VCF_PATH
from .config import NEXUS_FILES


def make_paths():
    """ Builds directories for cgap to use """
    directories = [FASTQ_PATH,
                   BLAST_PATH,
                   BAM_PATH,
                   VCF_PATH,
                   DEPTH_PATH,
                   CONSENSUS_FILES,
                   PHYLIP_FILES,
                   CODEML_PHYLIP_FILES]
    for directory in directories:
        if not os.path.isdir(directory):
            os.makedirs(directory)


def get_path(fasta_ref, fastq, directory, ext):
    """ builds the path of a file from config """
    fasta_name = os.path.basename(fasta_ref).rsplit(".", 1)[0]
    fastq_name = os.path.basename(fastq).rsplit(".", 1)[0]
    file_name = "{}.{}.{}".format(
        fasta_name,
        fastq_name,
        ext
    )
    path = os.path.join(directory, file_name)
    return path


def get_fastq_file_path(fasta_ref, fastq):
    """ builds the fastq file path """
    path = get_path(fasta_ref, fastq, FASTQ_PATH, "fastq")
    return path


def get_blast_file_path(fasta_ref, fastq):
    """ builds the blast file path """
    path = get_path(fasta_ref, fastq, BLAST_PATH, "blast")
    return path


def get_bam_file_working_path(fasta_ref, fastq):
    """ builds a duplicated bam working file """
    path = get_path(fasta_ref, fastq, BAM_PATH, "working.bam")
    return path


def get_bam_file_path(fasta_ref, fastq):
    """ gets the finalized bamfile path """
    path = get_path(fasta_ref, fastq, BAM_PATH, "bam")
    return path


def get_vcf_file_path(fasta_ref, fastq):
    """ gets the snp vcf path """
    path = get_path(fasta_ref, fastq, VCF_PATH, "vcf.gz")
    return path


def get_depth_file_path(fasta_ref, fastq):
    """ builds a depth file path for masking """
    path = get_path(fasta_ref, fastq, DEPTH_PATH, "tsv")
    return path


def get_cns_file_path(fasta_ref, fastq):
    """ builds a consensus file path """
    path = get_path(fasta_ref, fastq, CONSENSUS_FILES, "fa")
    return path


def get_phylip_file_path(fasta_ref):
    """ builds a consensus file path """
    directory = PHYLIP_FILES
    fasta_name = os.path.basename(fasta_ref).rsplit(".", 1)[0]
    file_name = "{}.{}".format(
        fasta_name,
        "phy"
    )
    path = os.path.join(directory, file_name)
    return path

def get_codeml_phylip_file_path(fasta_ref):
    """ builds a consensus file path """
    directory = CODEML_PHYLIP_FILES
    fasta_name = os.path.basename(fasta_ref).rsplit(".", 1)[0]
    file_name = "{}.{}".format(
        fasta_name,
        "relaxed.phy"
    )
    path = os.path.join(directory, file_name)
    return path


def get_nexus_file_path(fasta_ref):
    """ builds a consensus file path """
    directory = NEXUS_FILES
    fasta_name = os.path.basename(fasta_ref).rsplit(".", 1)[0]
    file_name = "{}.{}".format(
        fasta_name,
        "nex"
    )
    path = os.path.join(directory, file_name)
    return path


def get_blast_db_path(fastq):
    """ builds a blast database path """
    fastq_name = os.path.basename(fastq).rsplit(".", 1)[0]
    return fastq_name


def get_fastq_pair_name(fw_fq, rv_fq):
    """ combines forward and reverse fastq names """
    fq1 = os.path.basename(fw_fq).rsplit(".")[0]
    fq2 = os.path.basename(rv_fq).rsplit(".")[0]
    new_name = ""
    for num, items in enumerate(zip(fq1, fq2)):
        i, j = items
        if i == j:
            new_name += i
        else:
            if not num:
                new_name = "{}.{}".format(fq1, fq2)
            new_name += "."
            break
    return new_name
