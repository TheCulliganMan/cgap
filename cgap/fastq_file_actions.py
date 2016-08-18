#!/usr/bin/env python

def pair_fastq_files(forward, reverse):

    if len(forward) != len(reverse):
        return False

    for fw, rv in zip(forward, reverse):
        yield (fw, rv)
