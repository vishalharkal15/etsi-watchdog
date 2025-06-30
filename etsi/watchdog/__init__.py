# etsi/watchdog/__init__.py or drift_checker.py
from .drift.factory import get_drift_function
from .monitor import Monitor
from .compare import DriftComparator
from .drift.base import DriftResult

class DriftCheck:
    def __init__(self, reference_df, algorithm="psi", threshold=0.2):
        self.reference = reference_df
        self.algorithm = algorithm
        self.threshold = threshold
        self._func = get_drift_function(algorithm)

    def run(self, current_df, features):
        results = {}
        for feat in features:
            result = self._func(
                reference_df=self.reference,
                current_df=current_df,
                feature=feat,
                threshold=self.threshold
            )
            results[feat] = result
        return results

__all__ = ["DriftCheck", "Monitor", "DriftComparator", "DriftResult"]
