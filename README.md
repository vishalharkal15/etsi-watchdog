# etsi-watchdog

[![PyPI](https://img.shields.io/pypi/v/etsi-watchdog.svg)](https://pypi.org/project/etsi-watchdog/)
[![PyPI Downloads](https://static.pepy.tech/badge/etsi-watchdog)](https://pepy.tech/projects/etsi-watchdog)
[![Docs](https://etsi-ai.github.io/docs/etsi-watchdog.html)


**Real-time data drift detection for machine learning pipelines.**

`etsi-watchdog` is a production-ready Python library for drift detection, version comparison, and real-time monitoring of data streams. Designed for ML practitioners, data scientists, and AI engineers who need reliable data quality insights.


## Features
- PSI-based Drift Detection (more algorithms coming)

- Rolling Monitoring with time-frequency windowing
    
- Version Drift Comparison between model/data snapshots

- Built-in Visualization & JSON Export

- Minimal Dependencies & Fast Performance

- Clear API, suitable for both research and production

---

## Installation

```bash
pip install etsi-watchdog
```

---

## Quickstart


###  Drift Detection
```bash
from etsi.watchdog import DriftCheck
import pandas as pd

ref = pd.read_csv("reference.csv")
live = pd.read_csv("current.csv")

check = DriftCheck(ref)
results = check.run(live, features=["age", "salary"])

for feat, result in results.items():
    print(result.summary())
    result.plot()

```

### Rolling Monitoring
```bash

from etsi.watchdog import Monitor

monitor = Monitor(reference_df=ref)
monitor.enable_logging("logs/rolling_log.csv")

results = monitor.watch_rolling(
    df=live_data_stream,
    window=50,
    freq="D",
    features=["age", "salary"]
)

```


### Drift Comparison (A/B)
```bash
from etsi.watchdog import DriftComparator

check = DriftCheck(ref)
v1 = check.run(live1, features=["age", "salary"])
v2 = check.run(live2, features=["age", "salary"])

comp = DriftComparator(v1, v2)
print(comp.diff())

```

---

##  etsi-watchdog v3 — Roadmap & Vision

| Feature Area | Description |
|--------------|-------------|
|  **Multi-Algorithm Support** | Support for additional drift metrics:<br>- Jensen–Shannon Divergence (JSD)<br>- Wasserstein Distance<br>- Kolmogorov–Smirnov Test (K-S)<br>- Tree-based drift (e.g., `DeepDrift`) |
|  **Plug-in Architecture** | Drift algorithms will be fully plug-and-play. Custom metric support via `register_drift_function()` API. |
|  **Real-Time Stream Hooks** | Support for Kafka/Redis/WebSockets to detect drift on live data streams. |
|  **Concept Drift Detection** | Integration with models to detect label or concept drift, not just feature distribution shift. |
|  **CLI & YAML Configs** | Full CLI support:<br>`etsi-watchdog detect --ref ref.csv --live live.csv --features age salary`<br>+ YAML-based configuration for automated pipelines. |
|  **Benchmark Suite** | Built-in benchmarking with synthetic datasets to evaluate metric sensitivity and response time. |
|  **Dashboard UI (Optional)** | Lightweight dashboard (Streamlit/FastAPI) for monitoring drift over time visually. |
|  **Drift Summary Reports** | Generate PDF/HTML reports with drift summary, top features, histograms, and timestamps. |
|  **Sklearn & Pandas Integration** | `DriftCheck` will support `.fit()`/`.transform()` methods like Scikit-learn transformers. |

---


## 🤝 Contributing

Contributions are welcome. If you have an idea for a drift metric, integration, or improvement, please open an issue or PR on GitHub.
Please refer to [CONTRIBUTING.md](https://github.com/etsi-ai/etsi-watchdog/blob/main/CONTRIBUTING.md) for contribution guidelines and ensure





