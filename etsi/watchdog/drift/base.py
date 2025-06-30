#base
import warnings
import matplotlib.pyplot as plt

class DriftResult:
    def __init__(self, score: float, is_drifted: bool, details: dict, threshold: float = 0.2):
        self.drift_score = score
        self.is_drifted = is_drifted
        self.details = details
        self.threshold = threshold
        self._reference = None
        self._current = None

    def summary(self) -> str:
        status = "⚠️ Drift Detected" if self.is_drifted else "✅ No Significant Drift"
        return f"{status} | Drift Score: {self.drift_score:.4f} (Threshold: {self.threshold})"

    def plot(self):
        if self._reference is None or self._current is None:
            raise ValueError("Distributions not attached. Call `attach_distributions()` first.")
        import seaborn as sns
        import pandas as pd

        fig, axes = plt.subplots(len(self.details), 1, figsize=(7, 4 * len(self.details)))
        if len(self.details) == 1:
            axes = [axes]
        for i, feature in enumerate(self.details.keys()):
            ref = self._reference[feature]
            curr = self._current[feature]
            sns.kdeplot(ref, label="Reference", ax=axes[i])
            sns.kdeplot(curr, label="Current", ax=axes[i])
            axes[i].set_title(f"{feature} (Drift: {self.details[feature]:.4f})")
            axes[i].legend()
        plt.tight_layout()
        plt.show()

    def attach_distributions(self, reference_df, current_df):
        self._reference = reference_df
        self._current = current_df
