"""
etsi.watchdog — Lightweight Drift Monitoring

Main public interface for:
- DriftCheck: core drift detection logic
- Monitor: scheduled/rolling monitoring
- DriftComparator: compare drift across versions
- DriftResult: standard output object
"""

from .drift.factory import get_drift_function
from .monitor import Monitor
from .compare import DriftComparator
from .drift.base import DriftResult
import warnings


class DriftCheck:
    """
    DriftCheck — Compare reference vs current data for drift detection.

    Example:
    >>> check = DriftCheck(reference_df)
    >>> results = check.run(current_df, features=["age", "income"])
    """

    def __init__(self, reference_df, algorithm="psi", threshold=0.2):
        self.reference = reference_df
        self.algorithm = algorithm
        self.threshold = threshold
        self._func = get_drift_function(algorithm)

    def run(self, current_df, features):
        results = {}
        for feat in features:
            if feat not in self.reference.columns or feat not in current_df.columns:
                print(f"[watchdog] ⚠️ Skipping '{feat}' — missing in one of the datasets.")
                continue
            result = self._func(
                reference_df=self.reference,
                current_df=current_df,
                feature=feat,
                threshold=self.threshold
            )
            results[feat] = result
        return results

    def compare(self, *args, **kwargs):
        warnings.warn(
            "[watchdog] DriftCheck.compare() is deprecated, use .run(current_df, features) instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.run(*args, **kwargs)


__all__ = ["DriftCheck", "Monitor", "DriftComparator", "DriftResult"]
