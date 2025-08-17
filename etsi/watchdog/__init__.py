# etsi/watchdog/__init__.py

"""
etsi.watchdog — Lightweight Drift Monitoring

Exposes:
- DriftCheck: core drift checker
- Monitor: rolling drift monitor
- DriftComparator: compare two drift runs
- DriftResult: result object with summary, plot, and JSON support
- recap_results: generate comprehensive summary from multiple DriftResult objects
- print_results_recap: print formatted recap of drift results
"""

from .drift_check import DriftCheck
from .monitor import Monitor
from .compare import DriftComparator
from .drift.base import DriftResult
from .utils import recap_results, print_results_recap

__all__ = [
    "DriftCheck",
    "Monitor",
    "DriftComparator",
    "DriftResult",
    "recap_results",
    "print_results_recap",
]
