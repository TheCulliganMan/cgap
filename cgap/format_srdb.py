#!/usr/bin/env python
# -*- coding: utf-8 -*-

def format_srdb_cmds(file_name):
    cmd = ["perl", "bin/formatSRDB.pl", file_name]
    return cmd

def run_format_cmd(fastq):
    format_srdb_cmds(fastq)
    return sp.call(cmd)
