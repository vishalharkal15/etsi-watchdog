from scipy.stats import ks_2samp
from .base import DriftResult

def ks_drift(reference, current, feature):
    ref = reference[feature].dropna().values
    cur = current[feature].dropna().values

    stat, p_value = ks_2samp(ref, cur)

    return DriftResult(
        method="ks",
        score=1 - p_value,
        threshold=0.2,
        sample_size=len(cur),
        details={"ks_stat": stat, "p_value": p_value}
    )
