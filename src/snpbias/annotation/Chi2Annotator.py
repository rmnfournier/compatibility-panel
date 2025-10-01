from snpbias.annotation.Annotator import Annotator
from scipy.stats import chi2_contingency


class Chi2Annotator(Annotator):
    def __init__(self, df):
        super().__init__(df)
        if len(self.technologies) != 2:
            raise ValueError("The Chi2Annotator requires exactly two technologies.")

    def compute_score(self, row):
        contingency_table = self.build_contingency_table(row)
        chi2_stat, p_value = self.chi2_test(contingency_table)
        return p_value

    def build_contingency_table(self, row):
        """
        return a len(self.technologies) x 2 contingency table
        """
        table = []
        for tech in self.technologies:
            alt_count = row[f"alt_reads_{tech}"]
            ref_count = row[f"all_reads_{tech}"] - alt_count
            table.append([alt_count + 1, ref_count + 1])
        return table
    
    def chi2_test(self, table):
        chi2_stat, p_value, _, _ = chi2_contingency(table)
        return chi2_stat, p_value
