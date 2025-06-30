#ks
import numpy as np
from scipy.stats import ks_2samp
from .base import DriftResult

def ks_drift(ref, live, threshold=0.1):
    score = 0.0
    details = {}

    for col in ref.columns:
        stat, _ = ks_2samp(ref[col], live[col])
        details[col] = stat
        score = max(score, stat)

    return DriftResult(score=score, threshold=threshold, is_drifted=score > threshold, details=details)
