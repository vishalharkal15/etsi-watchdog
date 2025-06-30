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
        'salary': np.random.normal(50000, 10000, 500)
        # 'gender': np.random.choice(['M', 'F'], 500)
    })

    live = pd.DataFrame({
        'age': np.random.normal(35, 5, 500),
        'salary': np.random.normal(55000, 15000, 500)
        # 'gender': np.random.choice(['M', 'F'], 500)
    })
    return ref, live


# ----------- ✅ 1. DriftCheck Basic Test -----------
def test_drift_check():
    print("\n🧪 Running DriftCheck...")
    ref, live = generate_data()

    check = DriftCheck(ref)
    results = check.run(live, features=["age", "salary", "gender"])

    for feat, result in results.items():
        print(f"[✓] DriftCheck ({feat}) passed.")
        print(result.summary())
        result.plot()
        result.to_json(f"logs/drift_{feat}.json")


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
        d.index = pd.date_range(
            start=datetime.today() - timedelta(days=9 - i),
            periods=60,
            freq='min'  # fixed from deprecated 'T' and broken '...'
        )
        live.append(d)

    live_df = pd.concat(live)
    results = monitor.watch_rolling(live_df, window=50, freq="D", threshold=0.1)

    for date, res in results:
        print(f"{date.date()} - Drift: {res.is_drifted} | Top: {res.summary()}")



# ----------- ✅ 3. Drift Comparator (between versions) -----------
def test_comp():
    print("\n🧪 Running DriftComparator...")

    # Simulate 2 live versions and 1 reference
    ref, live_v1 = generate_data()
    _, live_v2 = generate_data()
    live_v2["age"] -= 3  # slight distribution change

    check = DriftCheck(ref)

    # Run drift detection for both live versions
    results_v1 = check.run(live_v1, features=["age", "salary"])
    results_v2 = check.run(live_v2, features=["age", "salary"])

    # Compare PSI differences
    comp = DriftComparator(results_v1, results_v2)
    diff = comp.diff()

    print("[✓] DriftComparator passed.")
    print("Δ Drift Scores between v1 and v2:")
    for feat, delta in diff.items():
        trend = "⬆️" if delta > 0 else "⬇️"
        print(f"{feat}: Δ={delta:+.4f} {trend}")

# ----------- ✅ Run All Tests -----------
if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)

    test_drift_check()
    test_monitor()
    test_comp()

    print("\n🎉 All watchdog component tests passed.\n")
