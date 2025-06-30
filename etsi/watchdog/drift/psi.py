#psi 

import numpy as np
import pandas as pd
from .base import DriftResult
import warnings

def compute_psi(expected: np.ndarray, actual: np.ndarray, bins=10) -> float:
    """Compute the PSI for a single feature."""
    try:
        expected_perc, _ = np.histogram(expected, bins=bins, range=(min(expected), max(expected)), density=True)
        actual_perc, _ = np.histogram(actual, bins=bins, range=(min(expected), max(expected)), density=True)

        expected_perc += 1e-6
        actual_perc += 1e-6

        psi = np.sum((expected_perc - actual_perc) * np.log(expected_perc / actual_perc))
        return psi
    except Exception:
        return 0.0

def psi_drift(reference: pd.DataFrame, current: pd.DataFrame, threshold: float = 0.2) -> DriftResult:
    if len(reference) < 50 or len(current) < 50:
        warnings.warn("PSI may be unreliable on samples < 50 rows", UserWarning)

    drift_details = {}
    total_psi = 0.0
    for column in reference.columns:
        if pd.api.types.is_numeric_dtype(reference[column]):
            psi = compute_psi(reference[column], current[column])
            drift_details[column] = psi
            total_psi += psi

    avg_psi = total_psi / len(drift_details) if drift_details else 0.0
    is_drifted = avg_psi > threshold
    result = DriftResult(score=avg_psi, is_drifted=is_drifted, details=drift_details, threshold=threshold)
    result.attach_distributions(reference, current)
    return result
