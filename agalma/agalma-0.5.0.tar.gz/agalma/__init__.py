# Agalma - Tools for processing gene sequence data and automating workflows
# Copyright (c) 2012-2014 Brown University. All rights reserved.
#
# This file is part of Agalma.
#
# Agalma is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Agalma is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Agalma.  If not, see <http://www.gnu.org/licenses/>.

"""
Agalma is an automated tool that constructs matrices for
phylogenomic analyses, allowing complex phylogenomic analyses to be
implemented and described unambiguously as a series of high-level
commands.  The user provides raw Illumina transcriptome data, and
Agalma produces annotated assemblies, aligned gene sequence matrices,
a preliminary phylogeny, and detailed diagnostics that allow the
investigator to make extensive assessments of intermediate analysis
steps and the final results.  Sequences from other sources, such as
externally assembled genomes and transcriptomes, can also be
incorporated in the analyses. Agalma is built on the BioLite
bioinformatics framework, which tracks provenance, profiles processor
and memory use, records diagnostics, manages metadata, installs
dependencies, logs version numbers and calls to external programs, and
enables rich HTML reports for all stages of the analysis. Agalma
includes a small test data set and a built-in test analysis of these
data.

See `__cite__` for information on citing Agalma.
"""

__cite__ = """Please cite Agalma as:

Dunn CW, Howison M, Zapata F. 2013. Agalma: an automated phylogenomics
workflow. BMC Bioinformatics 14(1): 330. doi:10.1186/1471-2105-14-330

Please cite BioLite as:

Howison M, Sinnott-Armstrong N, Dunn CW. 2012. BioLite, a lightweight
bioinformatics framework with automated tracking of diagnostics and provenance.
In Proceedings of the 4th USENIX Workshop on the Theory and Practice of
Provenance (TaPP '12), 14-15 June 2012, Boston, MA, USA.

The following programs are integral to Agalma and should also be cited:

Altschul SF, Madden TL, Schaffer AA, Zhang J, Zhang Z, Miller W, Lipman DJ.
1997. Gapped BLAST and PSI-BLAST: a new generation of protein database search
programs. Nucl Acids Res 25(17): 3389-3402. doi:10.1093/nar/25.17.3389

Andrews S. FastQC: A quality control tool for high throughput sequence data.
[http://www.bioinformatics.bbsrc.ac.uk/projects/fastqc/]

Dongen Sv and Abreu-Goodger C. 2012. Using MCL to Extract Clusters from
Networks. Methods in Molecular Biology. doi:10.1007/978-1-61779-361-5_15

Grabherr MG, Haas BJ, Yassour M, et al. 2011. Full-length transcriptome
assembly from RNA-Seq data without a reference genome. Nat Biotech 29(7):
644-652. doi:10.1038/nbt.1883

Langmead B, Salzberg SL. 2012. Fast gapped-read alignment with Bowtie 2.
Nature Methods 9(4): 357-359. doi:10.1038/nmeth.1923

Li B, Dewey CN. 2011. RSEM: accurate transcript quantification from RNA-Seq
data with or without a reference genome. BMC Bioinformatics 12(1): 323.
doi:10.1186/1471-2105-12-323

Katoh K, Standley DM. 2013. MAFFT Multiple Sequence Alignment Software Version
7: Improvements in Performance and Usability. Mol Biol Evol 30(4): 772-780.
doi:10.1093/molbev/mst010

Talavera G, Castresana J. 2007. Improvement of phylogenies after removing
divergent and ambiguously aligned blocks from protein sequence alignments.
Systematic Biology 54(4): 564-577. doi:10.1080/10635150701472164

Stamatakis A. 2006. RAxML-VI-HPC: maximum likelihood-based phylogenetic
analyses with thousands of taxa and mixed models. Bioinformatics 22(21):
2688-2690. doi:10.1093/bioinformatics/btl446

Tange, O. 2011. GNU Parallel - The Command-Line Power Tool. ;login: The
USENIX Magazine 36(1): 42-47.

"""

__version__ = "0.5.0"
