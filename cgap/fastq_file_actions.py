#!/usr/bin/env python

def pair_fastqs(forward_reads, reverse_reads):
    """ Yields pairs of fastq f / r files """
    for i, j in zip(forward_reads, reverse_reads):
        yield (i, j)
