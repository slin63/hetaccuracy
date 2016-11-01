import argparse
import os

# Default values
HWEFILTER_NAME = "bash HWEfiltering_phetexcessfilter.sh"
KEEP = "keep_seq.txt"
PVAL = 0.001
GATK = "final.GATK.vcf.recode.vcf"
GATKGZ = "final.GATK.vcf.recode.vcf.gz"

parser = argparse.ArgumentParser(description='Calls HWEfilter with the following arguments')
parser.add_argument('-KEEP', default=KEEP, help='Name of the keep file')
parser.add_argument('-GATK', default=GATK, help='Name of the GATK file')
parser.add_argument('-GATKGZ', default=GATKGZ, help='Name of the GATKGZ file')
parser.add_argument('-PVAL', default=PVAL, type=float, help='Pval to use for cutoff determination')

args = parser.parse_args()

import pdb; pdb.set_trace()  # breakpoint f497dd90 //


os.system("{} {} {} {} {}".format(
    HWEFILTER_NAME,
    args.KEEP,
    args.GATK,
    args.GATKGZ,
    args.PVAL
))




