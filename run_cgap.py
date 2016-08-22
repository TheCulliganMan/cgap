#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
import cgap
from multiprocessing import Pool


def cgap_parser():
    ''' parses command line arguments for cgap '''
    parser = argparse.ArgumentParser(
        description='Start cGAP: Script for running \
        Consensus Gene Assembly Program')

    parser.add_argument(
        '-refs_path',
        action = "store",
        dest = "refs_path",
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

    parser.add_argument(
        '-c',
        action = "store",
        dest = "cores",
        help = "Number of cores to run on",
        type = int,
        default = 1
    )  # number of cores

    args = parser.parse_args()

    return args.refs_path, args.forward_reads, args.reverse_reads, args.cores


def main():
    ''' runs all the steps in the cgap pipeline. '''
    # Setup for cgap run
    cgap.make_paths()
    refs_path, forward_reads, reverse_reads, cores = cgap_parser()
    fastas = list(cgap.get_fasta_paths(refs_path))

    # Create small fastqs
    format_commands = []
    blast_commands = []
    hit_commands = []

    for fastq in fastqs:
        format_commands.append(fastq)
        hit_commands.append((fastas, fastq))
        for fasta in fastas:
            blast_commands.append((fasta, fastq))

    p = Pool(cores)
    print("FORMATTING BLAST DATABASES...")
    p.map(cgap.run_format_cmd, format_commands)
    print("RUNNING BLAST...")
    p.map(cgap.run_blast_argslist, blast_commands)
    print("COLLECTING AND BINNING BLAST HITS")
    p.map(cgap.collect_hits_argslist, hit_commands)

    # generate consensus
    cns_commands = []
    for fasta in fastas:
        for fw_rd, rv_rd in cgap.pair_fastqs(forward_reads, reverse_reads):
                cns_commands.append((fasta, fw_rd, rv_rd))
    print("BUILDING CONSENSUS SEQUENCES")
    p.map(cgap.pipe_consensus_argslist, cns_commands)

if __name__ == '__main__':
    main()
