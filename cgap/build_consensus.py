#!/usr/bin/env python

from subprocess import Popen, PIPE


def bwa_mem_cmd(fasta_path, fw_fq, rv_fq):
    cmd = ['bwa', 'mem', fasta_path, fw_fq, rv_fq]
    return cmd


def samtools_view_cmd():
    cmd = ['samtools', 'view', '-Su', '-']
    return cmd


def novosort_cmd(output_bam_file):
    cmd = ['novosort',
           '-m', '1g',
           '-o', output_bam_file,
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


def cat_final_bam(bamfile_final):
    cmd = ['cat', bamfile_final]
    return cmd


def samtools_mpileup(ref_file):
    cmd = ['samtools', 'mpileup', 'A', '-ug',
           '-f', ref_file, '-s', '-']
    return cmd


def bcftools_call():
    cmd = ['bcftools', 'call', '-c']
    return cmd


def bgunzip():
    cmd = ['bgunzip']
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


def build_working_bam(ref_file, fw_fq, rv_fq):
    bwa_cmd = bwa_mem_cmd(ref_file, fw_fq, rv_fq)
    sam_cmd = samtools_view_cmd()
    nov_cmd = novosort_cmd(output_bam_file)

    p1 = Popen(bwa_cmd, stdout = PIPE)
    p2 = Popen(sam_cmd, stdin = p1.stdout, stdout = PIPE)
    p3 = Popen(nov_cmd, stdin = p2.stdout)

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
    buz_cmd = bgunzip()
    idx_cmd = tabix(vcf_file_out)

    with open(vcf_file_out, "w+") as output_handle:
        p1 = Popen(cat_cmd, stdout = PIPE)
        p2 = Popen(sam_cmd, stdin = p1.stdout, stdout = PIPE)
        p3 = Popen(bcf_cmd, stdin = p2.stdout, stdout = PIPE)
        p4 = Popen(buz_cmd, stdin = p3.stdout, stdout = output_handle)

    status = sp.call(idx_cmd)

    return True


def build_depth_file(vcf_file_out, depth_file):

    fil_cmd = bcftools_filter(vcf_file_out)
    que_cmd = bcftools_query()

    with open(depth_file, 'w+') as output_handle:
        p1 = Popen(fil_cmd, stdout=PIPE)
        p2 = Popen(que_cmd, stdin=p1.stdout, stdout=output_handle)

    return True


def build_consensus(vcf_file_out, ref_file, depth_file, cns_file):
    cns_cmd = ['bcftools',
               'consensus', vcf_file_out,
               '-f', ref_file,
               '-m', depth_file]

    with open(cns_file, 'w+') as output_handle:
        p1 = Popen(cns_cmd, stdout=output_handle)


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

    build_working_bam(ref_file, fw_fq, rv_fq)
    build_final_bam(bamfile_working, bamfile_final)
    build_vcf(ref_file, bamfile_final, vcf_file_out)
    build_depth_file(vcf_file_out, depth_file)
    build_consensus(vcf_file_out, ref_file, depth_file, cns_file)

    return True
