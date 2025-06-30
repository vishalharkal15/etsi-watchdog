import time
import pandas as pd
from .drift.factory import DriftCheck
from .logger import get_logger

logger = get_logger("monitor")

class Monitor:
    def __init__(self, interval_sec=60, algo="ks", threshold=0.1):
        self.interval_sec = interval_sec
        self.drift_check = DriftCheck(algo=algo, threshold=threshold)

    def run(self, ref_path, live_path):
        while True:
            ref = pd.read_csv(ref_path)
            live = pd.read_csv(live_path)
            result = self.drift_check.run(ref, live)
            logger.info(result)
            time.sleep(self.interval_sec)
