from .drift.factory import get_drift_function
from .monitor import Monitor
from .compare import DriftComparator
from .drift.base import DriftResult

class DriftCheck:
    def __init__(self, reference, algorithm="psi"):
        self.reference = reference
        self._func = get_drift_function(algorithm)


    def run(self, reference_df, current_df, features):
        results = {}
        for feat in features:
            result = self._func(reference_df, current_df, feat)
            results[feat] = result
        return results

__all__ = ["DriftCheck", "Monitor", "DriftComparator", "DriftResult"]
