#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .format_srdb import run_format_cmd
from .get_blast import run_blast
from .collect_hits import collect_hits
from .build_consensus import pipe_consensus

def test():
    run_format_cmd('../sm_test.1.fq')
    run_format_cmd('../sm_test.2.fq')
