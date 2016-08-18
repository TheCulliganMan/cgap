# -*- coding: utf-8 -*-
#!/usr/bin/env python
MarkDuplicatesJarPath = "/cGAP/bin/MarkDuplicates.jar"
import os
import subprocess as sp

def samtools_index_fasta(fasta_path):
    cmd = ['samtools', 'faidx', fasta_path]
    return cmd


def bwa_index_fasta(fasta_path):
    cmd = ['bwa', 'index', fasta_path]
    return cmd


def bwa_mem_cmd(fasta_path, fw_fq, rv_fq):
    cmd = ['bwa', 'mem', fasta_path, fw_fq, rv_fq]
    return cmd


def samtools_view_cmd():
    cmd = ['samtools', 'view', '-Su']
    return cmd


def novosort_cmd(bamfile_working):
    cmd = ['novosort',
           '-m', '1g',
           '-o', bamfile_working,
           '-t', '.', '-']
    return cmd


def mark_duplicates_cmd(bamfile_working, bamfile_final):
    cmd = ['java', '-jar', MarkDuplicatesJarPath,
           'INPUT={}'.format(bamfile_working),
           'OUTPUT={}'.format(bamfile_final),
           'REMOVE_DUPLICATES=true',
           'METRICS_FILE=dup.txt',
           'ASSUME_SORTED=true']
    return cmd


def samtools_index_bam_cmd(bamfile_final):
    cmd = ['samtools', 'index', bamfile_final]
    return cmd


def cat_final_bam(bamfile_final):
    cmd = ['cat', bamfile_final]
    return cmd


def samtools_mpileup(ref_file):
    cmd = ['samtools', 'mpileup', '-A', '-ug',
           '-f', ref_file, '-s', '-']
    return cmd


def bcftools_call():
    cmd = ['bcftools', 'sp.call', '-c']
    return cmd


def bgunzip():
    cmd = ['bgzip', '-d']
    return cmd


def tabix(vcf_file_out):
    cmd = ['tabix', '-f', vcf_file_out]
    return cmd


def bcftools_filter(vcf_file_out):
    cmd = ['bcftools', 'filter',
           "-i'(%QUAL<20)||(%QUAL==999)||(DP <= 3)'",
           vcf_file_out]
    return cmd


def bcftools_query():
    cmd = ['bcftools', 'query',
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
    cat_cmd = cat_final_bam(bamfile_final)
    sam_cmd = samtools_mpileup(ref_file)
    bcf_cmd = bcftools_call()
    #buz_cmd = bgunzip()
    idx_cmd = tabix(vcf_file_out)

    with open(vcf_file_out, "w+") as output_handle:
        p1 = sp.Popen(cat_cmd, stdout = sp.PIPE)
        p2 = sp.Popen(sam_cmd, stdin = p1.stdout, stdout = sp.PIPE)
        p3 = sp.Popen(bcf_cmd, stdin = p2.stdout, stdout = output_handle)
        #p4 = sp.Popen(buz_cmd, stdin = p3.stdout, stdout = output_handle)
        #p4.communicate()
        p3.communicate() #this will almost certainly have to change

    status = sp.call(idx_cmd)

    return True


def build_depth_file(vcf_file_out, depth_file):

    fil_cmd = bcftools_filter(vcf_file_out)
    que_cmd = bcftools_query()

    with open(depth_file, 'w+') as output_handle:
        p1 = sp.Popen(fil_cmd, stdout=sp.PIPE)
        p2 = sp.Popen(que_cmd, stdin=p1.stdout, stdout=output_handle)
        p2.communicate()

    return True


def build_consensus(vcf_file_out, ref_file, depth_file, cns_file):
    cns_cmd = ['bcftools',
               'consensus', vcf_file_out,
               '-f', ref_file,
               '-m', depth_file]

    with open(cns_file, 'w+') as output_handle:
        p1 = sp.Popen(cns_cmd, stdout=output_handle)
        p1.communicate()


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
    build_vcf(ref_file, bamfile_final, vcf_file_out)
    build_depth_file(vcf_file_out, depth_file)
    build_consensus(vcf_file_out, ref_file, depth_file, cns_file)

    return True

if __name__ == "__main__":
    pipe_consensus(
            "../Opn1mw.fa", #needs to be indexed first
            "../sm_test.1.fq",
            "../sm_test.2.fq",
            'bamfile_working.bam',
            'bamfile_final.bam',
            'vcf_file_out.vcf',
            'depth_file.tsv',
            'cns_file.fa'
        )
