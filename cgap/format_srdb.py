#!/usr/bin/env python

def format_srdb(reads):
    """
    Inputs:
        Read Files
    Returns:
        True
    Description:
        Makes commands to create a blast database.
    """
    format_commands = []
    for file_name in reads:
        format_commands.append("perl bin/formatSRDB.pl {file_name} ".format(**locals()))

    return format_commands
