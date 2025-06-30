import time
import pandas as pd
from . import DriftCheck

class Monitor:
    def __init__(self, ref_path, get_live_data_fn, features, interval_sec=3600, algo="psi"):
        self.reference = pd.read_csv(ref_path)
        self.get_live_data_fn = get_live_data_fn
        self.features = features
        self.checker = DriftCheck(algorithm=algo)
        self.interval = interval_sec

    def start(self):
        while True:
            current = self.get_live_data_fn()
            results = self.checker.run(self.reference, current, self.features)
            for feat, result in results.items():
                print(result.summary())
            time.sleep(self.interval)
