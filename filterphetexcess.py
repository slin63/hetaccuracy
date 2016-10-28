import pandas
import csv
import argparse

import variant_filter
# SAMPLE_CALL :: python filterphetexcess.py -vcf_list allsamplesafterfiltering.mpileup.vcf -pval_file out.hwe -amp_file ampliconregions.csv --pval 0.05

def to_drop(pval_file, vcf_file, amp_list, pval=0.05):
    tofilter = pandas.read_table(pval_file)
    loci = float(len(tofilter))
    print "NUM LOCI :: ", loci
    bonf = pval/loci
    print "CUTOFF   :: ", bonf

    drop_list_raw = tofilter[tofilter.P_HET_EXCESS <= bonf] # Rows to call FAILHW on

    header_line = get_lines_till_header(vcf_file)
    vcf_pd = pandas.read_table(vcf_file, skiprows=header_line)
    drop_list = variant_filter.process_to_drop(drop_list_raw, vcf_pd, amp_list) # Does that magic to check if > x% of variants fail and fails the rest.

    print "TO DROP  :: \n", drop_list[['CHR', 'POS']]

    return drop_list[['CHR', 'POS']]

def get_lines_till_header(vcf_file):
    header_line = 0
    with open(vcf_file, 'rb') as vcffile:
        vcf_reader = csv.reader(vcffile, delimiter='\t')
        line = 0
        for row in vcf_reader:
            if len(row) != 1:
                header_line = line
                break
            line += 1

    return header_line

def update_filter_status(vcf_file, drop_list):
    """Assigns FAILHW to rows listed in drop_list"""
    # http://stackoverflow.com/questions/26896382/how-to-search-pandas-data-frame-by-index-value-and-value-in-any-column
    header_line = get_lines_till_header(vcf_file)
    vcf_pd = pandas.read_table(vcf_file, skiprows=header_line)
    failed_count = 0

    # ah yes list comprehension -- the classic
    for index in drop_list.index:

        chrom = drop_list.loc[index]['CHR']
        pos = drop_list.loc[index]['POS']

        to_fail = vcf_pd[(vcf_pd['#CHROM'] == chrom ) & (vcf_pd['POS'] == pos)].index

        if len(to_fail) is 0:
            print '\t > CHROM: POS PAIR: {} NOT FOUND IN {}'.format(c_p, vcf_file)
            # raise KeyError('CHROM: POS PAIR: {} NOT FOUND IN {}'.format(c_p, vcf_file))
        else:
            failed_count += len(to_fail)

        vcf_pd.loc[to_fail, 'FILTER'] = 'FAILHW'

    print '\t >>> FAILED {} INDIVIDUAL ENTRIES FROM {} UNIQUE [CHROM: POS] KEYS'.format(failed_count, len(drop_list))

    return vcf_pd

def merge_old(vcf_file, updated_vcf, out_file):
    header_line = get_lines_till_header(vcf_file)
    with open(vcf_file, 'rb') as vcffile:
        first_half = list( csv.reader(vcffile, delimiter='\t') )[0:header_line]
        first_half = "\n".join([i[0] for i in first_half]) # Because the line above this returns a list of lists with only one element.
        other_half = updated_vcf.to_csv(sep='\t', index=False)

        merged_vcf = first_half + '\n' + other_half

    with open(out_file, 'wb') as merged_out:
        print "OUTFILE  :: ", out_file
        merged_out.write(merged_vcf)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update pass/fail values on the passed .VCF file.')
    parser.add_argument('-vcf_list', nargs='*', help='List with the names of the VCF files to be processed.')
    parser.add_argument('-pval_file', help='Name of the CSV file containing calculated p-vals')
    parser.add_argument('-amp_file', help='Name of the CSV file containing Amplicon data')
    parser.add_argument('--pval', type=float, help='Pval to use for cutoff determination')
    args = parser.parse_args()

    for vcf in args.vcf_list:
        OUT_NAME = "PHETE-FILTERED_"+ vcf
        amp_list = variant_filter.read_amp_file(args.amp_file)

        to_drop_list = to_drop(args.pval_file, vcf, amp_list, args.pval)
        updated_vcf = update_filter_status(vcf, to_drop_list)
        merge_old(vcf, updated_vcf, OUT_NAME)

