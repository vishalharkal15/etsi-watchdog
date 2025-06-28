# etsi-watchdog

[![PyPI](https://img.shields.io/pypi/v/etsi-watchdog.svg)](https://pypi.org/project/etsi-watchdog/)
[![PyPI Downloads](https://static.pepy.tech/badge/etsi-watchdog)](https://pepy.tech/projects/etsi-watchdog)

**Real-time data drift detection for machine learning pipelines.**

`etsi-watchdog` is a lightweight, plug-and-play Python package for detecting distribution shifts between training and production data. It helps ensure the stability of machine learning models in real-world environments with changing data.

---

## Installation

```bash
pip install etsi-watchdog
```

---

## What It Does

- Detects data drift using Population Stability Index (PSI)

- Works with both numeric and categorical features

- Supports rolling drift detection on time-based data

- Allows custom actions to be triggered on drift (e.g., alerts, retraining)

- Logs PSI and drift status to CSV for auditing

- Tracks top drifting features for prioritization

---

## What's New in v0.2.0

```bash
Full Changelog: [v0.1.1 → v0.2.0]
```

### Major Additions
✅ Rolling Drift Detection

 - Analyze PSI across time windows

✅ Top Drifting Features

 - Identify most impacted features with .top_features()

✅ CSV Logging

 - Logs all drift events and PSI scores

--- 

## Quick Example

```bash

import pandas as pd
from etsi.watchdog import DriftMonitor

# Reference dataset
ref = pd.DataFrame({
    "feature1": [1, 2, 3, 4, 5],
    "feature2": [100, 102, 101, 98, 99],
    "category": ["A", "B", "A", "C", "B"]
})

# Simulated live data with drift
live = pd.DataFrame({
    "feature1": [20, 21, 22, 23, 24],
    "feature2": [180, 181, 182, 183, 184],
    "category": ["Z", "Z", "Z", "Z", "Z"]
})

monitor = DriftMonitor(reference=ref)
monitor.enable_logging("logs/drift_log.csv")

result = monitor.watch(live)
print("Latest PSI:", result.psi)
print("Top features:", result.top_features(2))

result.on_drift(lambda: print("Drift detected"))


```

#### Sample Output

```bash

[watchdog] logs/ directory not found.
[watchdog] logs created at /project/logs

Latest PSI: {'category': 25.5211, 'feature2': 27.631, 'feature1': 25.903}
Top features: [('feature2', 27.631), ('feature1', 25.903)]
Drift detected.

```


#### Sample drift_log.csv Output

```bash

timestamp,drift,category,feature2,feature1
2025-06-27T22:30:29.645231,True,25.5211,27.631,25.903

```

---

## Rolling Drift Detection (Time Series)

```bash

rolling = monitor.watch_rolling(live_with_dates, window=5, freq="D")
for date, res in rolling:
    print(date, res.drift, res.top_features())

```

---

## Coming Soon in v0.2.1

 - Streamlit Dashboard
 - Drift Trend Plots
 - Snapshot Archiving


---

## Contributing

Contributions are welcome. If you have an idea for a drift metric, integration, or improvement, please open an issue or PR on GitHub.




