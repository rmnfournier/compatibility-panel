from abc import ABC, abstractmethod


class Annotator(ABC):
    def __init__(self, df):
        self.df = df
        self.technologies = self.infer_technologies()

    def infer_technologies(self):
        return list({
            column.removeprefix("all_reads_")
            for column in self.df.columns
            if column.startswith("all_reads_")
        })

    def annotate(self):
        df_results = self.df[["chr", "pos", "ref", "alt"]].copy()
        df_results["score"] = 0.0
        for ii, row in self.df.iterrows():
            score = self.compute_score(row)
            df_results.at[ii, "score"] = score
        return df_results

    @abstractmethod
    def compute_score(self, row):
        pass
