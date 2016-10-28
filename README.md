[![Codacy Badge](https://api.codacy.com/project/badge/Grade/1b52bcb34a74497fa04336c3234b8321)](https://www.codacy.com/app/rrculligan/cgap?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=TheCulliganMan/cgap&amp;utm_campaign=Badge_Grade)
# cgap
##What it is:
cgap is a gene extraction pipeline.  It deals with large fastq files by parsing
them with blast to speed bwa alignment on a reference file.  This amounts to
substantial time savings
##How it works:

![alt text][cgap workflow]
[cgap workflow]: media/cgap_graph.png "cgap workflow"
##How to use it:
1. Update or clone clone the cgap repository.
  * If you don't have cgap:

    ```bash

    git clone https://github.com/TheCulliganMan/cgap.git

    ```

  * If you want to update cgap:

    ```bash

    cd <cgap_dir>;
    git pull;

    ```
3. Use our docker image with the required binaries, or compile your own software.

  ```bash
  docker pull theculliganman/cgap:latest
  docker run -itv <your directory>:/work theculliganman/cgap /bin/bash
  ```
  Requirements:
  * python [python version: 3.5.1, anaconda: 2.5.0]
  * biopython [version: 1.66]
  * samtools [version: 1.3]
  * bcftools [version: 1.2]
  * htslib [version: 1.3]
  * bwa [version: 0.7.5-r405]
  * novosort [version: 1.03.03]
  * tabix [version: 0.2.5]
  * blastn [version: 2.2.28]

3. Make necessary changes to the [cgap config file](cgap/config.py)
```python
from os.path import abspath

CORES = int(6)

# WORK LOCATIONS
##Created in your current working directory
FASTQ_PATH = abspath("fastq_files")
HITS_PATH = abspath("hit_files")
HIT_FASTQ_PATH = abspath("hit_fastq_files")
BLAST_PATH = abspath('blast_files')
BAM_PATH = abspath('bam_files')
VCF_PATH = abspath('vcf_files')
DEPTH_PATH = abspath('depth_files')
CONSENSUS_FILES = abspath('consensus_files')
PHYLIP_FILES = abspath('phylip_files')

# PROGRAM LOCATIONS
MARK_DUPLICATES_JAR_PATH = "/bin/MarkDuplicates.jar"
SAMTOOLS_PATH = 'samtools'
BWA_PATH = 'bwa'
NOVOSORT_PATH = 'novosort'
TABIX_PATH = 'tabix'
BCFTOOLS_PATH = 'bcftools'

# QUALITY SETTINGS
## Minimum quality for bases to remain unmasked.
## Integers only!!!
MASK_MIN_QUALITY = int(20)

## Minimum depth for bases to remain unmasked.
## Integers only!!!
MASK_MIN_DEPTH = int(4)

## Minimum Blast Score #we used 50.0
MIN_BLAST_SCORE = float(50.0)
```

4. Run the cgap command.

  ```bash
  python run_cgap.py \
    -refs_path <directory where fastas are located> \
    -forward <fastq_1_fw> <fastq_1_fw> <fastq_1_fw> \
    -reverse <fastq_2_rv> <fastq_2_rv> <fastq_2_rv> \
    -c 5 \
    -format_db #[optional, only if they need formatting.]
  ```
  
  or in the form of a slurm script.

  ```bash
  #!/bin/sh

  #SBATCH --time=10:00:00          # Run time in hh:mm:ss
  #SBATCH --mem=50G        # Minimum memory required per CPU (in megabytes)
  #SBATCH --job-name=TortCgap
  #SBATCH --ntasks=8
  #SBATCH --error=/work/hdzoo/shared/cgap_bin/cgap/job.%J.err
  #SBATCH --output=/work/hdzoo/shared/cgap_bin/cgap/job.%J.out

  module load compiler/gcc/4.8
  module load bcftools/1.3
  module load blast/2.2
  module load bwa/0.7
  module load HTSlib/1.3
  module load python/3.5
  module load tabix/0.2
  module load novocraft
  module load samtools/1.3
  module load blast-legacy
  module load java/1.8

  export PATH=/home/hdzoo/shared/software/bin:$PATH

  python run_cgap.py \
    -refs_path galapagos_ref \
    -forward ab1tr1.fastq  ch1tr1.fastq  datr1.fastq  ep1tr1.fastq  m1tr1.fastq  p2tr1.fastq  va2tr1.fastq \
    -reverse ab1tr2.fastq  ch1tr2.fastq  datr2.fastq  ep1tr2.fastq  m1tr2.fastq  p2tr2.fastq  va2tr2.fastq \
    -c 8 -format_db;
  ```
