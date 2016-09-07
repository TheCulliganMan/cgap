#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess as sp

from Bio import SeqIO
from Bio.Seq import Seq

from .config import BCFTOOLS_PATH
from .config import BWA_PATH
from .config import MARK_DUPLICATES_JAR_PATH
from .config import NOVOSORT_PATH
from .config import SAMTOOLS_PATH
from .config import TABIX_PATH
from .make_paths import get_bam_file_path
from .make_paths import get_bam_file_working_path
from .make_paths import get_cns_file_path
from .make_paths import get_depth_file_path
from .make_paths import get_fastq_pair_name
from .make_paths import get_vcf_file_path
from .make_paths import get_fastq_file_path



def samtools_index_fasta(fasta_path):
    """ indexes a fasta with samtools """
    cmd = [SAMTOOLS_PATH, 'faidx', fasta_path]
    return cmd


def bwa_index_fasta(fasta_path):
    """ builds a bwa index for a fasta """
    cmd = [BWA_PATH, 'index', fasta_path]
    return cmd


def bwa_mem_cmd(fasta_path, fw_fq, rv_fq):
    """ bwa mem command builder """

    short_fw_fq = get_fastq_file_path(fasta_path, fw_fq)
    short_rv_fq = get_fastq_file_path(fasta_path, rv_fq)

    cmd = [BWA_PATH, 'mem', fasta_path, short_fw_fq, short_rv_fq]

    return cmd


def samtools_view_cmd():
    """ runs samtools view command builder"""
    cmd = [SAMTOOLS_PATH, 'view', '-Su']
    return cmd


def novosort_cmd(bamfile_working):
    """ novosort command builder """
    cmd = [NOVOSORT_PATH,
           '-m', '1g',
           '-o', bamfile_working,
           '-t', '.', '-']
    return cmd


def mark_duplicates_cmd(bamfile_working, bamfile_final):
    """ mark duplicates command builder """
    cmd = ['java', '-jar', MARK_DUPLICATES_JAR_PATH,
           'INPUT={}'.format(bamfile_working),
           'OUTPUT={}'.format(bamfile_final),
           'REMOVE_DUPLICATES=true',
           'METRICS_FILE=dup.txt',
           'ASSUME_SORTED=true']
    return cmd


def samtools_index_bam_cmd(bamfile_final):
    """ bamfile index command maker """
    cmd = [SAMTOOLS_PATH, 'index', bamfile_final]
    return cmd


def cat_final_bam(bamfile_final):
    """ cat command maker """
    cmd = ['cat', bamfile_final]
    return cmd


def samtools_mpileup(bamfile_final, ref_file):
    """ mpileup command maker """
    cmd = [SAMTOOLS_PATH, 'mpileup', '-A', '-ug',
           '-f', ref_file, '-s', bamfile_final]
    return cmd


def bcftools_call():
    """ bcftools call command maker """
    cmd = [BCFTOOLS_PATH, 'call', '-c']
    return cmd


def bgzip():
    """ bgzip command maker """
    cmd = ['bgzip', '-c']
    return cmd


def tabix(vcf_file_out):
    """ tabix command maker """
    cmd = [TABIX_PATH, '-f', '-p', 'vcf', vcf_file_out]
    return cmd


def bcftools_filter(vcf_file_out):
    """ bcftools commmand maker """
    filter_string = "-i'(%QUAL<{MASK_MIN_QUALITY})||(%QUAL==999)||(DP <= {MASK_MIN_DEPTH})'"
    cmd = [BCFTOOLS_PATH, 'filter',
           filter_string,
           vcf_file_out]
    return cmd


def bcftools_query():
    """ bcftools command maker """
    cmd = [BCFTOOLS_PATH, 'query',
           "-f'%CHROM\t%POS\n'"]
    return cmd


def get_fasta_record(fasta_path):
    """returns a single fasta file record"""
    with open(fasta_path) as input_handle:
        for record in SeqIO.parse(input_handle, 'fasta'):
            return record
    return False


def write_fasta_record(record, file_path):
    """writes a fasta file record"""
    with open(file_path, "w+") as output_handle:
        SeqIO.write(record, output_handle, 'fasta')
    return True


def remask_if_empty(fasta_ref, cns_path):
    """remasks the consensus if there is no file size."""
    if os.stat(cns_path).st_size:  # if file has a size
        return True

    record = get_fasta_record(fasta_ref)
    if record:
        new_seq = Seq("".join(["N" for char in record.seq]))
        record.seq = new_seq
        return write_fasta_record(record, cns_path)
    return False


def build_fasta_indices(fasta_path):
    """ builds fasta indices """
    bwa_cmd = bwa_index_fasta(fasta_path)
    sam_cmd = samtools_index_fasta(fasta_path)

    sp.call(bwa_cmd)
    sp.call(sam_cmd)
    return True


def build_working_bam(ref_file, fw_fq, rv_fq, bamfile_working):
    """ builds first step bamfile """

    bwa_cmd = bwa_mem_cmd(ref_file, fw_fq, rv_fq)
    sam_cmd = samtools_view_cmd()
    nov_cmd = novosort_cmd(bamfile_working)

    p1 = sp.Popen(bwa_cmd, stdout=sp.PIPE)
    p2 = sp.Popen(sam_cmd, stdin=p1.stdout, stdout=sp.PIPE)
    p3 = sp.Popen(nov_cmd, stdin=p2.stdout)

    status = p3.communicate()

    return status


def build_final_bam(bamfile_working, bamfile_final):
    """ builds finalized bamfile """
    dups_cmd = mark_duplicates_cmd(bamfile_working, bamfile_final)
    index_bam_cmd = samtools_index_bam_cmd(bamfile_final)

    sp.call(dups_cmd)
    sp.call(index_bam_cmd)

    os.remove(bamfile_working)
    return True


def build_vcf(ref_file, bamfile_final, vcf_file_out):
    """ builds snp vcf file to make consensus """
    sam_cmd = samtools_mpileup(bamfile_final, ref_file)
    bcf_cmd = bcftools_call()
    buz_cmd = bgzip()
    idx_cmd = tabix(vcf_file_out)

    with open(vcf_file_out, "w+") as output_handle:
        p1 = sp.Popen(sam_cmd, stdout=sp.PIPE)
        p2 = sp.Popen(bcf_cmd, stdin=p1.stdout, stdout=sp.PIPE)
        p3 = sp.Popen(buz_cmd, stdin=p2.stdout, stdout=output_handle)
        p3.communicate()

    sp.call(idx_cmd)

    return vcf_file_out


def build_depth_file(vcf_file_out, depth_file):
    """ builds depth tsv file for consensus masking """
    fil_cmd = bcftools_filter(vcf_file_out)
    que_cmd = bcftools_query()

    with open(depth_file, 'w+') as output_handle:
        p1 = sp.Popen(fil_cmd, stdout=sp.PIPE)
        p2 = sp.Popen(que_cmd, stdin=p1.stdout, stdout=output_handle)
        p2.communicate()

    return True


def build_consensus(vcf_file_out, ref_file, depth_file, cns_file):
    """ builds masked consensus file """
    cns_cmd = [BCFTOOLS_PATH,
               'consensus', vcf_file_out,
               '-f', ref_file,
               '-m', depth_file]

    with open(cns_file, 'w+') as output_handle:
        status = sp.call(cns_cmd, stdout=output_handle)

    return status


def pipe_consensus(fasta, fw_fq, rv_fq):
    """ runs all of the consensus commands in the right order """
    pair_name = get_fastq_pair_name(fw_fq, rv_fq)

    bamfile_working = get_bam_file_working_path(fasta, pair_name)
    bamfile_final = get_bam_file_path(fasta, pair_name)
    vcf_file_out = get_vcf_file_path(fasta, pair_name)
    depth_file = get_depth_file_path(fasta, pair_name)
    cns_file = get_cns_file_path(fasta, pair_name)

    build_fasta_indices(fasta)
    build_working_bam(fasta, fw_fq, rv_fq, bamfile_working)
    build_final_bam(bamfile_working, bamfile_final)
    vcf_file_out = build_vcf(fasta, bamfile_final, vcf_file_out)
    build_depth_file(vcf_file_out, depth_file)
    build_consensus(vcf_file_out, fasta, depth_file, cns_file)
    remask_if_empty(fasta, cns_file)

    return True


def pipe_consensus_argslist(args):
    """ runs the pipe consensus command with 1 argument """
    if len(args) == 3:
        fasta, fw_rd, rv_rd = args
        pipe_consensus(fasta, fw_rd, rv_rd)
        return True
    return False
