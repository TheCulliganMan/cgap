#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess as sp

from .config import MARK_DUPLICATES_JAR_PATH
from .config import SAMTOOLS_PATH
from .config import BWA_PATH
from .config import NOVOSORT_PATH
from .config import TABIX_PATH
from .config import BCFTOOLS_PATH
from .config import MASK_MIN_QUALITY
from .config import MASK_MIN_DEPTH


def samtools_index_fasta(fasta_path):
    cmd = [SAMTOOLS_PATH, 'faidx', fasta_path]
    return cmd


def bwa_index_fasta(fasta_path):
    cmd = [BWA_PATH, 'index', fasta_path]
    return cmd


def bwa_mem_cmd(fasta_path, fw_fq, rv_fq):
    cmd = [BWA_PATH, 'mem', fasta_path, fw_fq, rv_fq]
    return cmd


def samtools_view_cmd():
    cmd = [SAMTOOLS_PATH, 'view', '-Su']
    return cmd


def novosort_cmd(bamfile_working):
    cmd = [NOVOSORT_PATH,
           '-m', '1g',
           '-o', bamfile_working,
           '-t', '.', '-']
    return cmd


def mark_duplicates_cmd(bamfile_working, bamfile_final):
    cmd = ['java', '-jar', MARK_DUPLICATES_JAR_PATH,
           'INPUT={}'.format(bamfile_working),
           'OUTPUT={}'.format(bamfile_final),
           'REMOVE_DUPLICATES=true',
           'METRICS_FILE=dup.txt',
           'ASSUME_SORTED=true']
    return cmd


def samtools_index_bam_cmd(bamfile_final):
    cmd = [SAMTOOLS_PATH, 'index', bamfile_final]
    return cmd


def cat_final_bam(bamfile_final):
    cmd = ['cat', bamfile_final]
    return cmd


def samtools_mpileup(bamfile_final, ref_file):
    cmd = [SAMTOOLS_PATH, 'mpileup', '-A', '-ug',
           '-f', ref_file, '-s', bamfile_final]
    return cmd


def bcftools_call():
    cmd = [BCFTOOLS_PATH, 'call', '-c']
    return cmd


def bgzip():
    cmd = ['bgzip', '-c']
    return cmd


def tabix(vcf_file_out):
    cmd = [TABIX_PATH, '-f', '-p', 'vcf', vcf_file_out]
    return cmd


def bcftools_filter(vcf_file_out):
    filter_string = "-i'(%QUAL<{MASK_MIN_QUALITY})||(%QUAL==999)||(DP <= {MASK_MIN_DEPTH})'"
    cmd = [BCFTOOLS_PATH, 'filter',
           filter_string,
           vcf_file_out]
    return cmd


def bcftools_query():
    cmd = [BCFTOOLS_PATH, 'query',
           "-f'%CHROM\t%POS\n'"]
    return cmd


def build_fasta_indices(fasta_path):
    bwa_cmd = bwa_index_fasta(fasta_path)
    sam_cmd = samtools_index_fasta(fasta_path)

    sp.call(bwa_cmd)
    sp.call(sam_cmd)
    return True


def build_working_bam(ref_file, fw_fq, rv_fq, bamfile_working):
    bwa_cmd = bwa_mem_cmd(ref_file, fw_fq, rv_fq)
    sam_cmd = samtools_view_cmd()
    nov_cmd = novosort_cmd(bamfile_working)

    p1 = sp.Popen(bwa_cmd, stdout = sp.PIPE)
    p2 = sp.Popen(sam_cmd, stdin = p1.stdout, stdout=sp.PIPE)
    p3 = sp.Popen(nov_cmd, stdin = p2.stdout)
    status = p3.communicate()
    return True


def build_final_bam(bamfile_working, bamfile_final):
    dups_cmd = mark_duplicates_cmd(bamfile_working, bamfile_final)
    index_bam_cmd = samtools_index_bam_cmd(bamfile_final)

    sp.call(dups_cmd)
    sp.call(index_bam_cmd)

    os.remove(bamfile_working)
    return True


def build_vcf(ref_file, bamfile_final, vcf_file_out):
    sam_cmd = samtools_mpileup(bamfile_final, ref_file)
    bcf_cmd = bcftools_call()
    buz_cmd = bgzip()
    idx_cmd = tabix(vcf_file_out)

    with open(vcf_file_out, "w+") as output_handle:
        p1 = sp.Popen(sam_cmd, stdout = sp.PIPE)
        p2 = sp.Popen(bcf_cmd, stdin = p1.stdout, stdout = sp.PIPE)
        p3 = sp.Popen(buz_cmd, stdin = p2.stdout, stdout = output_handle)
        p3.communicate()

    status = sp.call(idx_cmd)

    return vcf_file_out


def build_depth_file(vcf_file_out, depth_file):

    fil_cmd = bcftools_filter(vcf_file_out)
    que_cmd = bcftools_query()

    with open(depth_file, 'w+') as output_handle:
        p1 = sp.Popen(fil_cmd, stdout=sp.PIPE)
        p2 = sp.Popen(que_cmd, stdin=p1.stdout, stdout=output_handle)
        p2.communicate()

    return True


def build_consensus(vcf_file_out, ref_file, depth_file, cns_file):
    cns_cmd = [BCFTOOLS_PATH,
               'consensus', vcf_file_out,
               '-f', ref_file,
               '-m', depth_file]

    with open(cns_file, 'w+') as output_handle:
        p1 = sp.call(cns_cmd, stdout=output_handle)

    return True


def pipe_consensus(
        ref_file,
        fw_fq,
        rv_fq,
        bamfile_working,
        bamfile_final,
        vcf_file_out,
        depth_file,
        cns_file
    ):

    build_fasta_indices(ref_file)
    build_working_bam(ref_file, fw_fq, rv_fq, bamfile_working)
    build_final_bam(bamfile_working, bamfile_final)
    vcf_file_out = build_vcf(ref_file, bamfile_final, vcf_file_out)
    build_depth_file(vcf_file_out, depth_file)
    build_consensus(vcf_file_out, ref_file, depth_file, cns_file)

    return True
