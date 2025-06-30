# etsi/watchdog/drift/shap_drift.py

from .base import DriftResult


def shap_drift(*args, **kwargs) -> DriftResult:
    raise NotImplementedError("SHAP-based drift detection coming in v0.4.")
