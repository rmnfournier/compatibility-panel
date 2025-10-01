from snpbias.annotation.Chi2Annotator import Chi2Annotator
from scipy.stats import chi2
import numpy as np


class BayesAnnotator(Chi2Annotator):
    def __init__(self, df):
        super().__init__(df)
        self.pseudo_count = 1

    def compute_score(self, row):
        contingency_table = self.build_contingency_table(row, pseudocount=self.pseudo_count)
        chi2_stat, p_value = self.chi2_test(contingency_table)
        p_data_invert = self.p_data_invert(contingency_table)
        p_data_under_h0 = chi2.pdf(chi2_stat, df=len(self.technologies) - 1)
        if p_data_invert == 0:
            return 0
        return p_data_under_h0 * p_data_invert

    def p_data_invert(self, contingency_table):
        contingency_table = np.array(contingency_table)
        p_data_invert = np.prod(np.sum(contingency_table, axis=1) - self.pseudo_count * contingency_table.shape[1])
        return p_data_invert
