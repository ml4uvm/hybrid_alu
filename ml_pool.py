import csv
from itertools import cycle


class MLTestPool:
    """
    Handles ML-prioritized / clustered testcase pool
    """

    def __init__(self, file_path):
        self.testcases = self._load_testcases(file_path)
        if not self.testcases:
            raise ValueError("ML pool is empty!")

        self.iterator = cycle(self.testcases)

    def _load_testcases(self, file_path):
        """
        Load clustered/prioritized testcases from CSV
        Uses: opcode, a_type, b_type
        Ignores: gain_label, predicted_gain, cluster (for now)
        """
        testcases = []

        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)

            for row in reader:
                testcase = {
                    "opcode": int(row["opcode"]),
                    "a_type": int(row["a_type"]),
                    "b_type": int(row["b_type"]),
                    # optional debug info
                    "predicted_gain": float(row["predicted_gain"]),
                    "cluster": int(row["cluster"]),
                }
                testcases.append(testcase)

        return testcases

    def get_next(self):
        return next(self.iterator)