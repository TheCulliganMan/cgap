# cgap

##What it is:
cgap is a gene extraction pipeline.  It deals with large fastq files by parsing
them with blast to speed bwa alignment on a reference file.  This amounts to
substantial time savings
##How it works:
blast => hits files => bwa => (samtools, bcftools, novosort) => consensus sequence.
##How to use it:
1. First clone the repository.

  ```bash
  git clone https://github.com/TheCulliganMan/cgap.git
  ```

3. Use our docker image with the required binaries, or compile your own software.

  ```bash
  docker pull theculliganman/cgap
  docker run -itv <your directory>:/work theculliganman/cgap /bin/bash
  ```
  Requirements:
  1. samtools
  2. bcftools
  3. bwa
  4. novosort
  5. tabix
  6. blast
  7. biopython


3. Run the cgap command.

  ```bash
  python cgap.py \
    -refs_path <directory where fastas are located> \
    -forward <fastq_1_fw> <fastq_1_fw> <fastq_1_fw> \
    -reverse <fastq_2_rv> <fastq_2_rv> <fastq_2_rv>
  ```
