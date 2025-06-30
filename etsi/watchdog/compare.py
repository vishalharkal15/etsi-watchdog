import json

class DriftComparator:
    def __init__(self, path_v1, path_v2):
        self.v1 = self._load(path_v1)
        self.v2 = self._load(path_v2)

    def _load(self, path):
        with open(path, "r") as f:
            return json.load(f)

    def compare(self):
        report = {}
        for key in self.v1:
            diff = self.v2.get(key, 0) - self.v1.get(key, 0)
            report[key] = {"v1": self.v1.get(key), "v2": self.v2.get(key), "delta": diff}
        return report
