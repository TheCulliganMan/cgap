#!/usr/bin/env python
from os.path import basename

from get_blast import make_blast_commands
from format_srdb import format_srdb
from get_hits import make_hits_commands
from build consensus import pipe_consensus

def create_file_names():
    blast_file = '{read}.{s}.{n}.blast'.format(**locals())
