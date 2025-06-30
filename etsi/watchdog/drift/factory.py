from .ks import ks_drift
from .psi import calculate_psi
from .shap_drift import shap_drift

class DriftCheck:
    def __init__(self, algo="ks", threshold=0.1):
        self.algo = algo.lower()
        self.threshold = threshold
        self._algos = {
            "ks": ks_drift,
            "psi": calculate_psi,
            "shap": shap_drift
        }
        if self.algo not in self._algos:
            raise ValueError(f"Unsupported drift algo: {self.algo}")

    def run(self, ref, live):
        return self._algos[self.algo](ref, live, threshold=self.threshold)
