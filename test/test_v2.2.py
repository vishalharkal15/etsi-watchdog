import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

from etsi.watchdog import DriftCheck, Monitor, DriftComparator

# ---------- 🔧 Helper ----------
def generate_data():
    np.random.seed(42)
    ref = pd.DataFrame({
        "age": np.random.normal(30, 5, 500),
        "salary": np.random.normal(50000, 10000, 500)
    })
    live = pd.DataFrame({
        "age": np.random.normal(35, 5, 500),
        "salary": np.random.normal(54000, 12000, 500)
    })
    return ref, live

# ---------- ✅ 1. DriftCheck ----------
def test_drift_check():
    print("\n🧪 Running DriftCheck...")
    ref, live = generate_data()
    check = DriftCheck(ref)
    results = check.run(live, features=["age", "salary"])

    for feat, result in results.items():
        print(f"[✓] DriftCheck ({feat}) passed.")
        print(result.summary())
        result.plot()
        result.to_json(f"logs/drift_{feat}.json")

# ---------- ✅ 2. Monitor ----------
def test_monitor():
    print("\n🧪 Running DriftMonitor...")
    ref, _ = generate_data()
    monitor = Monitor(ref)
    monitor.enable_logging("logs/rolling_drift.csv")

    drifted_data = []
    for i in range(10):
        d = pd.DataFrame({
            "age": np.random.normal(30 + i, 5, 60),
            "salary": np.random.normal(50000 + i * 200, 10000, 60)
        })
        d.index = pd.date_range(datetime.today() - timedelta(days=9 - i), periods=60, freq='min')
        drifted_data.append(d)

    live_df = pd.concat(drifted_data)
    results = monitor.watch_rolling(live_df, window=50, freq="D")

    for date, res in results:
        print(f"{date.date()} → Drifted: {[f for f, r in res.items() if r.is_drifted]}")

# ---------- ✅ 3. Comparator ----------
def test_comparator():
    print("\n🧪 Running DriftComparator...")
    ref, _ = generate_data()
    live1 = pd.DataFrame({
        "age": np.random.normal(33, 5, 500),
        "salary": np.random.normal(52000, 12000, 500)
    })
    live2 = pd.DataFrame({
        "age": np.random.normal(30, 5, 500),  # improved
        "salary": np.random.normal(51000, 12000, 500)
    })

    check = DriftCheck(ref)
    r1 = check.run(live1, features=["age", "salary"])
    r2 = check.run(live2, features=["age", "salary"])

    comp = DriftComparator(r1, r2)
    diff = comp.diff()

    print("[✓] DriftComparator passed.")
    print("Δ Drift Scores:")
    for k, v in diff.items():
        print(f"{k}: {v:+.4f}")

# ---------- 🧪 Run all ----------
if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    test_drift_check()
    test_monitor()
    test_comparator()
    print("\n🎉 All watchdog tests passed successfully!\n")
