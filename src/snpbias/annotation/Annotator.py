from abc import ABC, abstractmethod
from tqdm import tqdm


class Annotator(ABC):
    def __init__(self, df, technologies=None):
        self.df = df
        if technologies is None:
            self.technologies = self.infer_technologies()
        else:
            self.technologies = self.check_if_technologies_are_present(technologies)
        print("Building annotations based on technologies:", self.technologies)

    def infer_technologies(self):
        return list({
            column.removeprefix("all_reads_")
            for column in self.df.columns
            if column.startswith("all_reads_")
        })

    def check_if_technologies_are_present(self, technologies):
        technologies = list(technologies)
        if not technologies:
            raise ValueError("No technologies provided.")
        missing = [
            tech for tech in technologies
            if f"all_reads_{tech}" not in self.df.columns
        ]
        if missing:
            missing_cols = ", ".join(f"all_reads_{tech}" for tech in missing)
            raise ValueError(f"Missing columns for technologies: {missing_cols}.")
        return technologies

    def annotate(self):
        df_results = self.df[["chr", "pos", "ref", "alt"]].copy()
        df_results["score"] = 0.0
        for ii, row in tqdm(self.df.iterrows(), total=self.df.shape[0]):
            score = self.compute_score(row)
            df_results.at[ii, "score"] = score
        return df_results

    @abstractmethod
    def compute_score(self, row):
        pass
