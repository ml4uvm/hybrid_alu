import pandas as pd
import os
import random
from pyuvm import uvm_sequence
from tb.sequences.sequence_item import ALUSeqItem

# 🔥 Hybrid imports
from hybrid.hybrid_selector import select_mode
from hybrid.ml_pool import MLTestPool


class ALUSequence(uvm_sequence):

    def __init__(self, name="ALUSequence", num_tests=300, use_ml=False):
        super().__init__(name)
        self.num_tests = num_tests
        self.use_ml = use_ml

    def generate_value(self, t):
        if t == "ZERO":
            return 0
        elif t == "SMALL":
            return random.randint(1, 9)
        elif t == "LARGE":
            return random.randint(100, 100)
        elif t == "NEG":
            return random.randint(-20, -1)

    async def body(self):

        base_dir = os.path.dirname(__file__)
        csv_path = os.path.join(base_dir, "../../ml/clustered_tests.csv")

        # Load ML test pool
        ml_pool = MLTestPool(csv_path)

        reverse_map = {
            0: "ZERO",
            1: "SMALL",
            2: "LARGE",
            3: "NEG"
        }

        # =========================================================
        # BASELINE MODE
        # =========================================================
        if not self.use_ml:
            print(f"[BASELINE MODE] Running {self.num_tests} random tests")

        # =========================================================
        # HYBRID MODE
        # =========================================================
        else:
            print(f"[HYBRID MODE] Running {self.num_tests} tests")

        for i in range(self.num_tests):

            # =========================================================
            # BASELINE MODE (pure random)
            # =========================================================
            if not self.use_ml:
                mode = "random"

            # =========================================================
            # HYBRID MODE (ML + random)
            # =========================================================
            else:
                mode = select_mode()

            item = ALUSeqItem("item")

            # =========================================================
            # ML TESTCASE
            # =========================================================
            if mode == "ml":

                tc = ml_pool.get_next()

                item.opcode = tc["opcode"]

                a_type = reverse_map[tc["a_type"]]
                b_type = reverse_map[tc["b_type"]]

                item.a = self.generate_value(a_type)
                item.b = self.generate_value(b_type)

                # Optional debug
                # print(f"[ML] opcode={item.opcode}, a={item.a}, b={item.b}")

            # =========================================================
            # RANDOM TESTCASE
            # =========================================================
            else:

                item.randomize()

                # Optional debug
                # print(f"[RANDOM] opcode={item.opcode}, a={item.a}, b={item.b}")

            # Store mode for logging
            item.mode = mode

            await self.start_item(item)
            await self.finish_item(item)