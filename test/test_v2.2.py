import pandas as pd
import numpy as np
from etsi.watchdog import DriftCheck, Monitor, DriftComparator
from datetime import datetime, timedelta
import os

# ----------- 🔧 Generate Sample Data -----------
def generate_data():
    np.random.seed(42)
    ref = pd.DataFrame({
        'age': np.random.normal(30, 5, 500),
        'salary': np.random.normal(50000, 10000, 500),
        'gender': np.random.choice(['M', 'F'], 500)
    })

    live = pd.DataFrame({
        'age': np.random.normal(35, 5, 500),
        'salary': np.random.normal(55000, 15000, 500),
        'gender': np.random.choice(['M', 'F'], 500)
    })
    return ref, live


# ----------- ✅ 1. DriftCheck Basic Test -----------
def test_drift_check():
    print("\n🧪 Running DriftCheck...")
    ref, live = generate_data()

    check = DriftCheck(ref)
    result = check.compare(live, algo="psi", threshold=0.2)

    assert hasattr(result, "psi")
    assert isinstance(result.is_drifted, bool)

    print("[✓] DriftCheck PSI passed.")
    print(result.summary())

    result.plot()  # Optional plot
    result.to_json("logs/drift_log.json")
    result.to_csv("logs/drift_log.csv")


# ----------- ✅ 2. Drift Monitoring (rolling) -----------
def test_monitor():
    print("\n🧪 Running DriftMonitor...")
    ref, _ = generate_data()

    monitor = Monitor(ref)
    monitor.enable_logging("logs/rolling_log.csv")

    # Simulate 10 days of drift
    live = []
    for i in range(10):
        d = pd.DataFrame({
            'age': np.random.normal(30 + i, 5, 60),
            'salary': np.random.normal(50000 + i * 200, 10000, 60),
            'gender': np.random.choice(['M', 'F'], 60)
        })
        d.index = pd.date_range(start=datetime.today() - timedelta(days=9 - i), periods=60, freq='T')
        live.append(d)

    live_df = pd.concat(live)
    results = monitor.watch_rolling(live_df, window=50, freq="D", threshold=0.1)

    for date, res in results:
        print(f"{date.date()} - Drift: {res.is_drifted} | Top: {res.top_features(2)}")


# ----------- ✅ 3. Drift Comparator (between versions) -----------
def test_comparator():
    print("\n🧪 Running DriftComparator...")
    _, live1 = generate_data()
    _, live2 = generate_data()
    # add some improvement
    live2['age'] = live2['age'] - 2

    ref, _ = generate_data()

    check = DriftCheck(ref)
    r1 = check.compare(live1, algo="psi")
    r2 = check.compare(live2, algo="psi")

    comp = DriftComparator(r1, r2)
    diff = comp.diff()

    print("[✓] DriftComparator passed.")
    print("Δ PSI between v1 and v2:")
    for k, v in diff.items():
        print(f"{k}: {v:+.4f}")


# ----------- ✅ Run All Tests -----------
if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)

    test_drift_check()
    test_monitor()
    test_comparator()

    print("\n🎉 All watchdog component tests passed.\n")
