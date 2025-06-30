import json
import matplotlib.pyplot as plt
from dataclasses import dataclass, asdict


@dataclass
class DriftResult:
    method: str
    score: float
    threshold: float
    details: dict
    sample_size: int

    @property
    def is_drifted(self) -> bool:
        return self.score > self.threshold

    def summary(self) -> str:
        status = "🚨 Drift Detected!" if self.is_drifted else "✅ No Drift"
        return f"[{self.method.upper()}] Drift Score: {self.score:.4f} (threshold: {self.threshold}) — {status}"

    def plot(self):
        """Plot reference vs. current distribution using bar chart if details available."""
        if all(k in self.details for k in ["bins", "expected_percents", "actual_percents"]):
            bins = self.details["bins"]
            expected = self.details["expected_percents"]
            actual = self.details["actual_percents"]

            width = 0.35
            x = range(len(bins))

            plt.figure(figsize=(10, 5))
            plt.bar(x, expected, width, label='Reference')
            plt.bar([i + width for i in x], actual, width, label='Current')
            plt.xticks([i + width / 2 for i in x], bins, rotation=45)
            plt.ylabel('Percentage')
            plt.title(f"{self.method.upper()} Drift Distribution")
            plt.legend()
            plt.tight_layout()
            plt.show()
        else:
            print("[watchdog] 📉 No distribution info available to plot.")

    def to_json(self, path: str = None) -> dict:
        """Returns result as dict or writes to JSON file if path is provided."""
        data = asdict(self)
        if path:
            with open(path, "w") as f:
                json.dump(data, f, indent=2)
            print(f"[watchdog] ✅ DriftResult written to {path}")
        return data
