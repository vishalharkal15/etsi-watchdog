import json
import os
import pandas as pd

def log_drift(result_dict, path: str):
    rows = []
    for feat, result in result_dict.items():
        row = {
            "feature": feat,
            "score": result.score,
            "threshold": result.threshold,
            "is_drifted": result.is_drifted,
            "sample_size": result.sample_size
        }
        rows.append(row)

    df = pd.DataFrame(rows)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    if path.endswith(".json"):
        df.to_json(path, orient="records", indent=2)
    else:
        df.to_csv(path, index=False)
    print(f"[watchdog] ✅ DriftResult written to {path}")
