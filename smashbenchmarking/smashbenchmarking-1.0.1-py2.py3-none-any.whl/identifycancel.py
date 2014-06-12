from __future__ import print_function

import sys
import vcf

from parsers.vcfwriter import VCFWriter

def infoToStr(info):
    if len(info) == 0:
        return '.'
    else:
        return ";".join(map(lambda (k,v): str(k)+"="+str(v), info.iteritems()))

def genotype(vcfrecord):
    if not vcfrecord.samples:
        return "."
    # return {0 : "0/0", 1 : "0/1", 2: "1/1", None : "."}[vcfrecord.samples[0].gt_type]
    # PyVCF's gt_type field only contains the values above. Pass the actual gt string through
    # to avoid converting other values, e.g. "2/1" to "0/1"
    if vcfrecord.samples[0].gt_type == 1:
        return vcfrecord.samples[0].gt_nums
    return {0 : "0/0", 1 : "0/1", 2: "1/1", None : "."}[vcfrecord.samples[0].gt_type]

def write(record, writer):
    return writer.write_record(record.CHROM, record.POS, '.',
                               record.REF, ','.join(map(lambda a: str(a),record.ALT)), record.samples[0].gt_nums,infoToStr(record.INFO)) # TODO: more gtypes.

def add_var(variant, var_dict):
    if var_dict.has_key(variant.CHROM):
        if var_dict[variant.CHROM].has_key(variant.POS):
            var_dict[variant.CHROM][variant.POS].append(variant)
        else:
            var_dict[variant.CHROM][variant.POS] = [variant]
    else:
        var_dict[variant.CHROM] = {variant.POS:[variant]}

mergecount = 0
cancelcount = 0


def process_match(var_one, var_two):
  mergecount = 0
  cancelcount = 0
  ref_one = var_one.REF
  ref_two = var_two.REF
  alt_one = var_one.ALT[0]
  alt_two = var_two.ALT[0]

  if ref_one == alt_two and ref_two == alt_one:
    gt_one = var_one.samples[0].gt_nums
    gt_two = var_two.samples[0].gt_nums
    if gt_one == gt_two:
        # genotypes are the same, variants cancel out
        cancelcount += 1
    elif gt_one == '0|1' and gt_two == '1|1':
        # output 1|0 with gt_two's variant
        mergecount += 1
        output_var = var_two
        output_var.samples[0].gt_nums = '1|0'
        write(output_var,vcf_writer)
    elif gt_one == '1|1' and gt_two == '0|1':
        # output 1|0 with gt_one's variant
        mergecount += 1
        output_var = var_one
        output_var.samples[0].gt_nums = '1|0'
        write(output_var,vcf_writer)
    elif gt_one == '1|0' and gt_two == '1|1':
        # output 0|1 with gt_two's variant
        mergecount += 1
        output_var = var_two
        output_var.samples[0].gt_nums = '0|1'
        write(output_var,vcf_writer)
    elif gt_one == '1|1' and gt_two == '1|0':
        # output 0|1 with gt_one's variant
        mergecount += 1
        output_var = var_one
        output_var.samples[0].gt_nums = '0|1'
        write(output_var,vcf_writer)
    else:
        # write both variants back out
        write(var_one,vcf_writer)
        write(var_two,vcf_writer)
  else:
    # write both variants out
    write(var_one,vcf_writer)
    write(var_two,vcf_writer)
  return mergecount,cancelcount


if __name__ == "__main__":
    vcf_reader = vcf.Reader(open(sys.argv[1],'r'))
    ref = sys.argv[2]
    vcf_writer = VCFWriter(ref,'myvcf',sys.stdout)
    var_dict = {}
    mergecounter = 0
    cancelcounter = 0
    for r in vcf_reader:
        add_var(r,var_dict)
    for chrom in sorted(var_dict.keys()):
        for pos in sorted(var_dict[chrom].keys()):
            if len(var_dict[chrom][pos]) == 2:
                mergecount, cancelcount = process_match(var_dict[chrom][pos][0],var_dict[chrom][pos][1])
                mergecounter += mergecount
                cancelcounter += cancelcounter
            else:
                for r in var_dict[chrom][pos]:
                    write(r,vcf_writer)
    print("merge count ", mergecounter)
    print("cancel count ", cancelcounter)
