# etsi/watchdog/logger.py

import os
import json
from datetime import datetime

def log_drift(result, path):
    """Log DriftResult summary to a JSON file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)

    log_data = {
        "timestamp": datetime.now().isoformat(),
        "drift": result.is_drifted,
        "score": result.score,
        "details": result.details
    }

    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_data) + "\n")

    print(f"[watchdog] Drift log saved → {path}")
