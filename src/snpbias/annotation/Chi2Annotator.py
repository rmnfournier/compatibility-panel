from snpbias.annotation.Annotator import Annotator
from scipy.stats import chi2_contingency
from scipy.stats import PermutationMethod


class Chi2Annotator(Annotator):
    def __init__(self, df):
        super().__init__(df)

    def compute_score(self, row):
        contingency_table = self.build_contingency_table(row)
        chi2_stat, p_value = self.chi2_test(contingency_table)
        return p_value

    def build_contingency_table(self, row, pseudocount=0):
        """
        return a len(self.technologies) x 2 contingency table
        """
        table = []
        for tech in self.technologies:
            alt_count = row[f"alt_reads_{tech}"]
            ref_count = row[f"all_reads_{tech}"] - alt_count
            table.append([alt_count + pseudocount, ref_count + pseudocount])
        return table
    
    def chi2_test(self, table):
        if any(sum(row) == 0 for row in table) or any(sum(col) == 0 for col in zip(*table)):
            return 0, 1
        elif any(cell < 5 for row in table for cell in row):
            chi2_stat, p_value, _, _ = chi2_contingency(table, correction=False, method=PermutationMethod())
        else:
            chi2_stat, p_value, _, _ = chi2_contingency(table, correction=False)
        return chi2_stat, p_value
