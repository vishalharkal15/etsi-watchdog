#factor

from .psi import psi_drift
from .ks import ks_drift  # assume implemented similarly
# from .shap_drift import shap_drift  # placeholder

def get_drift_function(algo: str = "psi"):
    if algo == "psi":
        return psi_drift
    elif algo == "ks":
        return ks_drift
    # elif algo == "shap":
    #     return shap_drift
    else:
        raise ValueError(f"Unsupported drift algorithm: {algo}")
