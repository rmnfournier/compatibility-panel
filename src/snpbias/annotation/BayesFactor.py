from snpbias.annotation.Chi2Annotator import Chi2Annotator
from scipy.special import betaln
import numpy as np


class BayesFactor(Chi2Annotator):
    def __init__(self, df, technologies=None):
        super().__init__(df, technologies=technologies)
        self.alpha = 2
        self.beta = 2

    def compute_score(self, row):
        contingency_table = np.array(self.build_contingency_table(row, pseudocount=0))
        
        col_sums = np.sum(contingency_table, axis=0)
        K_total = col_sums[1]
        Alt_total = col_sums[0]
        
        log_prob_h0 = betaln(K_total + self.alpha, Alt_total + self.beta)
        
        log_prob_h1_terms = betaln(contingency_table[:, 1] + self.alpha, contingency_table[:, 0] + self.beta)
        log_prob_h1_sum = np.sum(log_prob_h1_terms)
                
        n_tech = len(self.technologies)
        log_b22 = betaln(self.alpha, self.beta)
        
        log_bf = log_prob_h0 - log_prob_h1_sum + (n_tech - 1) * log_b22
        
        return log_bf
