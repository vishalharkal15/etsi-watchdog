import pandas as pd
from .logger import log_drift
from typing import List

class Monitor:
    def __init__(self, reference):
        self.reference = reference
        self.log_path = None

    def enable_logging(self, path: str):
        self.log_path = path

    def watch(self, live: pd.DataFrame, threshold=0.2, algo="psi"):
        from .drift.factory import get_drift_function
        from . import DriftCheck  # 🔁 Lazy import to avoid circular

        checker = DriftCheck(self.reference, algorithm=algo, threshold=threshold)
        result = checker.run(live, features=self.reference.columns)


        if self.log_path:
            log_drift(result, self.log_path)
        return result

    def watch_rolling(self, live: pd.DataFrame, window=50, freq="D", threshold=0.2, algo="psi"):
        if not isinstance(live.index, pd.DatetimeIndex):
            raise ValueError("Live data must have a DatetimeIndex for rolling drift.")

        results = []
        for date, group in live.groupby(pd.Grouper(freq=freq)):
            if len(group) >= window:
                res = self.watch(group.tail(window), threshold=threshold, algo=algo)
                results.append((date, res))
        return results
