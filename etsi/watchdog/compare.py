import json

class DriftComparator:
    def __init__(self, result1=None, result2=None):
        self.result1 = result1
        self.result2 = result2

    def compare_logs(self, log1_path, log2_path):
        with open(log1_path) as f1, open(log2_path) as f2:
            run1 = json.load(f1)
            run2 = json.load(f2)

        print("\n🔍 Drift Comparison Report (Logs)")
        for feat in run1:
            if feat in run2:
                score1 = run1[feat]["score"]
                score2 = run2[feat]["score"]
                delta = score2 - score1
                trend = "⬆️" if delta > 0 else "⬇️"
                print(f"{feat}: v1={score1:.3f} → v2={score2:.3f} {trend} Δ={delta:.3f}")

    def diff(self):
        if not self.result1 or not self.result2:
            raise ValueError("Both results must be set for in-memory comparison.")

        scores1 = self.result1.details
        scores2 = self.result2.details

        delta = {}
        for feat in scores1:
            if feat in scores2:
                delta[feat] = round(scores2[feat] - scores1[feat], 4)
        return delta
