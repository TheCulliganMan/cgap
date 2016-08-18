def get_hits_commands(blast_file):

    cmd = "python bin/getHits.py -blastFile {} -n 50; ".format(blast_file)

    return cmd
