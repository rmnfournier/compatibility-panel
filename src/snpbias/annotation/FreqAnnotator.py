from snpbias.annotation.Annotator import Annotator


class FreqAnnotator(Annotator):
    def __init__(self, df, technologies=None):
        super().__init__(df, technologies=technologies)
        if len(self.technologies) != 2:
            raise ValueError("The FreqAnnotator requires exactly two technologies.")

    def compute_score(self, row):
        frequencies = {}
        for tech in self.technologies:
            if row[f"all_reads_{tech}"] == 0:
                return 1
            alt_freq = row[f"alt_reads_{tech}"] / row[f"all_reads_{tech}"]
            frequencies[tech] = alt_freq
        tech1, tech2 = self.technologies
        score = abs(frequencies[tech1] - frequencies[tech2])
        return score
