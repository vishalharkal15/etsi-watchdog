# etsi-watchdog 🐶

**A versatile tool for detecting dataset drift and monitoring data consistency in your ML pipelines.**

---

## 📌 What is etsi-watchdog?

**etsi-watchdog** is a data drift detection toolkit that helps ML practitioners and data engineers monitor whether their datasets have changed over time in ways that may impact model performance.

It supports **static drift checks**, **rolling window monitoring**, and **version comparison**, making it suitable for both real-time systems and batch workflows.

---

## 🚀 Why use etsi-watchdog?

- ✅ Detect when incoming data diverges from training data
- 📉 Prevent silent ML model degradation
- 🔁 Monitor data pipelines in production
- 🔍 Compare different dataset versions before deployment

---

## 🧠 High-Level Architecture

The tool revolves around three main components:

### 1. **DriftCheck** – Static drift detection
Compares two static datasets and reports statistical differences.

**Workflow:**
- Input: `reference_dataset.csv`, `current_dataset.csv`
- Calculates drift using metrics like KS-test, JS divergence
- Outputs a detailed report of drift per feature

---

### 2. **Monitor** – Rolling window detection
Continuously monitors incoming data and checks for drift against a reference.

**Workflow:**
- Maintains a rolling window of recent data
- Compares each new window to a reference
- Can be scheduled or integrated into real-time systems

---

### 3. **DriftComparator** – Version comparison
Compares two dataset versions (e.g., `v1 vs v2`) to assess changes before production pushes.

**Workflow:**
- Input: `version_1.csv`, `version_2.csv`
- Highlights changed distributions, added/removed features, and metrics

---

## 📦 Installation

```bash
pip install etsi-watchdog
```

Or install from source:

```bash
git clone https://github.com/<org>/etsi-watchdog.git
cd etsi-watchdog
pip install -e .
```

---

## 📘 Usage

### Static Drift Check

```python
from etsi_watchdog import DriftCheck

dc = DriftCheck(reference="data/train.csv", current="data/test.csv")
report = dc.run()
report.save("drift_report.html")
```

### Monitoring

```python
from etsi_watchdog import Monitor

monitor = Monitor(reference="data/baseline.csv", window_size=100)
monitor.feed(new_data_batch)
```

### Version Comparison

```python
from etsi_watchdog import DriftComparator

comparator = DriftComparator("data/v1.csv", "data/v2.csv")
comparator.compare().save("version_diff_report.html")
```

---

## 📊 Example Output

<p align="center">
  <img src="assets/drift_report_sample.png" width="700"/>
</p>

---

## 📂 Project Structure

```text
etsi_watchdog/
├── drift/
│   ├── drift_check.py
│   ├── monitor.py
│   └── comparator.py
├── utils/
├── tests/
├── README.md
└── setup.py
```

---

## 📄 Documentation

Full documentation is available [here](https://your-docs-link.com)

---

## 🤝 Contributing

We welcome contributions! Please:

- Check for open [issues](https://github.com/<org>/etsi-watchdog/issues)
- Create a new branch (`feature/your-feature`)
- Open a PR with clear description

If you're unsure where to start, comment on an issue, and a maintainer will help guide you.

---

## 📬 Contact

- Maintainer: [@maintainer_github](https://github.com/maintainer_github)
- LinkedIn: [Mentor LinkedIn](https://linkedin.com/in/mentor-profile)

---

## 📝 License

MIT License. See `LICENSE` for more info.
