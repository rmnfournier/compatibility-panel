from snpbias.parser.SNPParser import SNPParser


class CountParser(SNPParser):
    def annotate_snp(self, snp, snp_id):
        parser = self.initialize_parser(snp)
        counts = self.get_het_reads_for_snp(snp)
        for tech in self.technologies:
            total = counts[tech][0] + counts[tech][1]
            parser[f'all_reads_{tech}'] = int(total)
            parser[f'alt_reads_{tech}'] = int(counts[tech][1])
        return parser
