import json

class DriftComparator:
    def compare(self, log1_path, log2_path):
        with open(log1_path) as f1, open(log2_path) as f2:
            run1 = json.load(f1)
            run2 = json.load(f2)

        print("\n🔍 Drift Comparison Report")
        for feat in run1:
            if feat in run2:
                score1 = run1[feat]["score"]
                score2 = run2[feat]["score"]
                delta = score2 - score1
                trend = "⬆️" if delta > 0 else "⬇️"
                print(f"{feat}: v1={score1:.3f} → v2={score2:.3f} {trend} Δ={delta:.3f}")
