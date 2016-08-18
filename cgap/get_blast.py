#!/usr/bin/env python
import subprocess as sp

def run_blast(blast_db, query, output_file):

    cmd = ['blastall',
           '-p', 'blastn',
           '-d', blast_db,
           '-i', query,
           '-v', '500000',
           '-m', '8']

    with open(output_file, "w+") as output_handle
        status = sp.call(cmd, stdout=output_handle)

    return status
