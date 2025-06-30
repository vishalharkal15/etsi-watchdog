# factory.py
from .psi import psi_drift
from .ks import ks_drift
from .shap_drift import shap_drift

def get_drift_function(algo: str):
    if algo == "psi":
        return psi_drift
    elif algo == "ks":
        return ks_drift
    elif algo == "shap":
        return shap_drift
    else:
        raise ValueError(f"[watchdog] Unknown drift algorithm: '{algo}'")
