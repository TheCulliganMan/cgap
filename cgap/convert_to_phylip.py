#!/usr/bin/env python

from Bio import SeqIO, Seq

from .make_paths import get_cns_file_path
from .make_paths import get_fastq_pair_name
from .make_paths import get_phylip_file_path
from .make_paths import get_codeml_phylip_file_path


def get_cns_files_for_fasta(fasta, fw_fqs, rv_fqs):
    """ yeilds cns information for a given fasta """
    for fw_fq, rv_fq in zip(fw_fqs, rv_fqs):
        fq_pair = get_fastq_pair_name(fw_fq, rv_fq)
        cns_file = get_cns_file_path(fasta, fq_pair)
        yield (cns_file, fq_pair)


def read_fasta_record(file_path):
    """ returns the contents of a cgap fasta file """
    with open(file_path) as input_handle:
        for record in SeqIO.parse(input_handle, 'fasta'):
            record.seq = Seq.Seq(str(record.seq).replace("N","?"))
            return record
    return False


def yield_fasta_records(cns_path_list):
    """ yields fasta records to biopython for writing """
    for cns_file, fq_pair in cns_path_list:
        record = read_fasta_record(cns_file)
        if record:
            record.id = fq_pair
            yield record


def write_phylip_file(phylip_file, fasta_records_gen):
    """ writes seq records into a phylip file """
    with open(phylip_file, 'w+') as output_handle:
        SeqIO.write(fasta_records_gen, output_handle, 'phylip')
    return True

def write_codeml_phylip_file(codeml_phylip_file, fasta_records_gen):
    """ writes seq records into a phylip file """
    with open(phylip_file, 'w+') as output_handle:
        for record in fasta_records_gen:
            output_handle.write("{}    {}".format(record.id, record.seq))
    return True


def build_phylip_records(fasta, fw_fqs, rv_fqs):
    """ runs the phylip conversion and merge pipe """
    phylip_file = get_phylip_file_path(fasta)
    codeml_phylip_file = get_codeml_phylip_file_path(fasta)
    cns_file_gen = get_cns_files_for_fasta(fasta, fw_fqs, rv_fqs)
    fasta_records_gen = yield_fasta_records(cns_file_gen)
    write_phylip_file(phylip_file, fasta_records_gen)
    write_codeml_phylip_file(codeml_phylip_file, fasta_records_gen)
    return True


def build_phylip_records_argslist(args):
    """ runs the phylip conversion merge pipe with one arg """
    if len(args) == 3:
        fasta, fw_fqs, rv_fqs = args
        build_phylip_records(fasta, fw_fqs, rv_fqs)
        return True
    return False
