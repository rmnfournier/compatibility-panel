import argparse


def get_arguments():
    parser = argparse.ArgumentParser(description="Annotate SNPs in a VCF file")
    parser.add_argument('--vcf', type=str, help='Input imputed VCF file', required=True)
    parser.add_argument('--out', type=str, help='Output file', required=True)
    parser.add_argument('--ind', type=str, help='File with genetic ids (ind.tech)', required=True)
    parser.add_argument('--method', type=str, choices=['count'], default='count',
                        help='Annotation method to use')
    parser.add_argument('--test', action='store_true', help='Run in test mode (only 100 SNPs)')
    args = parser.parse_args()
    return args


def get_snp_parser(args):
    if args.method == 'count':
        from snpbias.parser.CountParser import CountParser
        parser = CountParser(vcf_file=args.vcf, ind_file=args.ind, output_file=args.out,
                             test_mode=args.test)
    else:
        raise ValueError(f"Method {args.method} not recognized")
    return parser


def main():
    args = get_arguments()
    snp_parser = get_snp_parser(args)
    snp_parser.run_parser()
