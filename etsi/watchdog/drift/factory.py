from .psi import psi_drift
from .ks import ks_drift

def get_drift_function(algo):
    if algo == "psi":
        return psi_drift
    elif algo == "ks":
        return ks_drift
    else:
        raise ValueError(f"[watchdog] Unknown drift algorithm: {algo}")
