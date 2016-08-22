# cgap_v2

##What it is:
cgap is a gene extraction pipeline.  It deals with large fastq files by parsing
them with blast to speed bwa alignment on a reference file.  This amounts to
substantial time savings
##How it works:
blast => hits files => bwa => (samtools, bcftools, novosort) => consensus sequence.
##How to use it:
1. First clone the repository.

```bash
git clone
```

2. Run the cgap command.

```bash
python cgap.py \
  -refs_path <directory where fastas are located> \
  -forward <fastq_1.1> <fastq_1.2> <fastq_1.3> \
  -reverse <fastq_2.1> <fastq_2.2> <fastq_2.3>
```
