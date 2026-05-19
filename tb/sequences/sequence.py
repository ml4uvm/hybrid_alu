import pandas as pd
import os
import random

from pyuvm import uvm_sequence

from tb.sequences.sequence_item import ALUSeqItem

# =========================================================
# Hybrid imports
# =========================================================

from hybrid.hybrid_selector import select_mode
from hybrid.ml_pool import MLTestPool

# =========================================================
# Coverage tracking imports
# =========================================================

from tb.components.env import (
    get_last_gain_label,
    is_coverage_complete
)

# =========================================================
# Hybrid configuration imports
# =========================================================

from hybrid.hybrid_config import (
    STAGNATION_THRESHOLD,
    ENABLE_EARLY_STOP
)


class ALUSequence(uvm_sequence):

    def __init__(
        self,
        name="ALUSequence",
        num_tests=300,
        use_ml=False
    ):
        super().__init__(name)

        self.num_tests = num_tests

        self.use_ml = use_ml

    # =========================================================
    # Operand generator
    # =========================================================

    def generate_value(self, t):

        if t == "ZERO":
            return 0

        elif t == "SMALL":
            return random.randint(1, 9)

        elif t == "LARGE":
            return random.randint(100, 100)

        elif t == "NEG":
            return random.randint(-20, -1)

    # =========================================================
    # Main sequence body
    # =========================================================

    async def body(self):

        # =====================================================
        # BASELINE MODE
        # =====================================================

        if not self.use_ml:

            print(
                f"[BASELINE MODE] "
                f"Running {self.num_tests} random tests"
            )

        # =====================================================
        # HYBRID MODE
        # =====================================================

        else:

            print(
                f"[HYBRID MODE] "
                f"Running adaptive hybrid execution"
            )

            base_dir = os.path.dirname(__file__)

            csv_path = os.path.join(
                base_dir,
                "../../ml/clustered_tests.csv"
            )

            # Load ML testcase pool
            ml_pool = MLTestPool(csv_path)

            reverse_map = {
                0: "ZERO",
                1: "SMALL",
                2: "LARGE",
                3: "NEG"
            }

            # 🔥 NEW
            consecutive_no_gain = 0

        # =====================================================
        # Main execution loop
        # =====================================================

        for i in range(self.num_tests):

            # =================================================
            # Early saturation stop
            # =================================================

            if ENABLE_EARLY_STOP:

                if is_coverage_complete():

                    print(
                        "[HYBRID] Coverage saturation reached. "
                        "Stopping early."
                    )

                    break

            # =================================================
            # BASELINE MODE
            # =================================================

            if not self.use_ml:

                mode = "random"

            # =================================================
            # HYBRID MODE
            # =================================================

            else:

                # 🔥 Exploration only after stagnation
                stagnated = (
                    consecutive_no_gain >=
                    STAGNATION_THRESHOLD
                )

                mode = select_mode(
                    stagnated=stagnated
                )

            item = ALUSeqItem("item")

            # =================================================
            # ML testcase
            # =================================================

            if mode == "ml":

                tc = ml_pool.get_next()

                item.opcode = tc["opcode"]

                a_type = reverse_map[
                    tc["a_type"]
                ]

                b_type = reverse_map[
                    tc["b_type"]
                ]

                item.a = self.generate_value(a_type)

                item.b = self.generate_value(b_type)

            # =================================================
            # RANDOM testcase
            # =================================================

            else:

                item.randomize()

            # =================================================
            # Store execution mode
            # =================================================

            item.mode = mode

            await self.start_item(item)

            await self.finish_item(item)

            # =================================================
            # Hybrid stagnation tracking
            # =================================================

            if self.use_ml:

                gain = get_last_gain_label()

                if gain == 0:

                    consecutive_no_gain += 1

                else:

                    consecutive_no_gain = 0