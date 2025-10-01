import argparse
from snpbias.annotation.FreqAnnotator import FreqAnnotator
from snpbias.annotation.Chi2Annotator import Chi2Annotator
from snpbias.annotation.BayesAnnotator import BayesAnnotator
import pandas as pd


def get_arguments():
    parser = argparse.ArgumentParser(description="Calculate SNP bias annotations from count data")
    parser.add_argument('--input', type=str, help='Input file with count data by technology', required=True)
    parser.add_argument('--out', type=str, help='Output file', required=True)
    parser.add_argument('--method', type=str, choices=['freq', 'chi2', 'bayes'], required=True,
                        help='Annotation method to use')
    args = parser.parse_args()
    return args


def get_snp_annotator(args):
    df = pd.read_csv(args.input, sep=',')
    if args.method == 'freq':
        annotator = FreqAnnotator(df)
    elif args.method == 'chi2':
        annotator = Chi2Annotator(df)
    elif args.method == 'bayes':
        annotator = BayesAnnotator(df)
    return annotator


def main():
    args = get_arguments()
    annotator = get_snp_annotator(args)
    df = annotator.annotate()
    df.to_csv(args.out, sep=',', index=False)
