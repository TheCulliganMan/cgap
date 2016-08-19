#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
import cgap

fastqs = ['sm_test.1.fq','sm_test.2.fq']
fastas = ['Opn1mw.fa']

def cgap_parser():

    parser = argparse.ArgumentParser(
        description='Start cGAP: Script for running \
        Consensus Gene Assembly Program')

    parser.add_argument(
        '-refs_path',
        action = "store",
        dest = "directory",
        help = "The path where cGAP gene references are stored.",
        required = True
    )  # Directory of query files

    parser.add_argument(
        '-forward',
        action = "store",
        dest = "forward_reads",
        nargs = "+",
        help = "The FORWARD fastq samples that will be \
        used for the run.",
        required = True
    )

    parser.add_argument(
        '-reverse',
        action = "store",
        dest = "reverse_reads",
        nargs = "+",
        help = "The REVERSE fastq samples that will be used \
        for this run.",
        required = True
    )  # Reverse Short Read Files

    args = parser.parse_args()

    all_fastqs = args.forward + args.reverse
    paired_fastqs = [(i,j) for i,j in zip(args.forward_reads,args.reverse_reads)]

def main():
    # Setup for cgap run
    cgap.make_paths()

    # Create small fastqs
    for fastq in fastqs:
        cgap.run_format_cmd(fastq)
        for fasta in fastas:
            cgap.run_blast(fasta, fastq)
        cgap.collect_hits([fasta], fastq)

    # generate consensus
    cgap.pipe_consensus(fastas[0], fastqs[0], fastqs[1])
