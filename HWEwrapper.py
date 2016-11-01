import argparse
import os

HWEFILTER_NAME = "bash HWEfiltering_phetexcessfilter.sh"

parser = argparse.ArgumentParser(description='Calls HWEfilter with the following arguments')
parser.add_argument('-KEEP', help='Name of the keep file')
parser.add_argument('-GATK', help='Name of the GATK file')
parser.add_argument('-GATKGZ', help='Name of the GATKGZ file')
parser.add_argument('-PVAL', type=float, help='Pval to use for cutoff determination')

args = parser.parse_args()

if None in args.__dict__.values():
    raise KeyError("Not enough arguments")
else:
    os.system("{} {} {} {} {}".format(
        HWEFILTER_NAME,
        args.KEEP,
        args.GATK,
        args.GATKGZ,
        args.PVAL
    ))



# KEEP=keep_seq.txt
# PVAL=0.001
# GATK=final.GATK.vcf.recode.vcf
# GATKGZ=final.GATK.vcf.recode.vcf.gz
