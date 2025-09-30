import numpy as np
import pandas as pd
import vcf


class SNPParser:
    def __init__(self, vcf_file: str, ind_file: str, output_file: str,
                 correct_posterior=True, posterior_threshold=0.9, test_mode=False):
        self.posterior_threshold = posterior_threshold
        self.vcf_reader = self.read_vcf(vcf_file)
        self.vcf_file = vcf_file
        self.samples = self.load_samples(ind_file)
        self.technologies = self.get_technologies()
        self.posterior_must_be_corrected = correct_posterior
        self.run_in_test_mode = test_mode
        self.min_reads_on_site = 1
        self.output_file = output_file
        self.initialize_method()

    def initialize_method(self):
        pass

    def read_vcf(self, filename):
        vcf_reader = vcf.Reader(filename=filename, compressed=True)
        return vcf_reader

    def load_samples(self, ind_file):
        df = pd.read_csv(ind_file, header=None, sep=" ")
        df[['master_id', 'tech']] = df[0].str.rsplit('.', n=1, expand=True)
        return df

    def get_technologies(self):
        technologies = [tech for tech in np.unique(self.samples["tech"].values)]
        return technologies

    def run_parser(self):
        valid_snp_id = 0
        results = []
        for snp in self.vcf_reader:
            if not self.snp_has_sufficient_reads(snp, self.min_reads_on_site):
                continue
            parser = self.annotate_snp(snp, valid_snp_id)
            results.append(parser)
            valid_snp_id += 1
            if valid_snp_id > 100 and self.run_in_test_mode:
                break
        df = pd.DataFrame(results)
        print(f"Saving file in {self.output_file}")
        df.to_csv(self.output_file, index=False)
        return df

    def snp_has_sufficient_reads(self, snp, min_reads):
        try:
            return snp.INFO['AC'][0] > min_reads
        except (KeyError, IndexError, AttributeError):
            # In some instances, weird errors happen with the VCF parser
            # I keep these SNPs in case.
            return True

    def annotate_snp(self, snp, snp_id):
        pass

    def initialize_parser(self, snp):
        parser = {
            'chr': snp.CHROM,
            'pos': snp.POS,
            'ref': snp.REF,
            'alt': snp.ALT[0],
        }
        return parser

    def get_tech_from_sample(self, sample):
        tech = sample.sample.split(".")[-1]
        return tech

    def calculate_posterior(self, sample):
        try:
            posterior = sample.data.GP
            if self.posterior_must_be_corrected:
                emission = self.convert_phred_to_emissions(sample.data.PL)
                posterior /= emission
                posterior = posterior / np.sum(posterior)
        except AttributeError:
            posterior = np.array((1. / 3, 1. / 3, 1. / 3))
        return posterior

    @staticmethod
    def convert_phred_to_emissions(pl):
        if pl:
            pl = np.array(pl)
            lh = 10. ** (-pl / 10)
            p_ref = lh[0] + 0.5 * lh[1]
            p_alt = lh[2] + 0.5 * lh[1]
            z = p_ref + p_alt
            p_ref /= z
            p_alt /= z

            p_ref_ref = p_ref * lh[0] / (lh[0] + lh[1])
            p_ref_alt = p_ref * lh[1] / (lh[0] + lh[1])
            p_alt_ref = p_alt * lh[1] / (lh[2] + lh[1])
            p_alt_alt = p_alt * lh[2] / (lh[2] + lh[1])

            posterior = (p_ref_ref, p_ref_alt + p_alt_ref, p_alt_alt)
            return np.array(posterior)
        else:
            return np.array([1. / 3, 1. / 3, 1. / 3])

    @staticmethod
    def sample_has_reads(sample):
        try:
            return sample.data.AD is not None
        except AttributeError:
            return False

    @staticmethod
    def get_reads(sample):
        if SNPParser.sample_has_reads(sample):
            reads = sample.data.AD
        else:
            reads = np.array((0, 0))
        return reads

    def get_het_reads_for_snp(self, snp):
        reads = {tech: np.zeros(2, dtype=float) for tech in self.technologies}
        for sample in snp.samples:
            if self.is_sample_heterozygous(sample):
                tech = self.get_tech_from_sample(sample)
                reads[tech] += np.array(sample.data.AD)
        return reads

    def is_sample_heterozygous(self, sample):
        if self.sample_has_reads(sample):
            if sample.data.AD is None:
                return False
            posterior = self.calculate_posterior(sample)
            try:
                return posterior[1] > self.posterior_threshold
            except IndexError:
                return False
        return False
