import random
from hybrid.hybrid_config import (
    EPSILON,
    USE_DYNAMIC_EPSILON,
    COVERAGE_THRESHOLD,
    EPSILON_LOW,
    EPSILON_HIGH,
    MIN_EPSILON,
    MAX_EPSILON,
    DEBUG_PRINT
)


def get_epsilon(current_coverage=None):
    """
    Returns epsilon value (static or dynamic)
    """

    if not USE_DYNAMIC_EPSILON:
        return EPSILON

    # Dynamic epsilon based on coverage
    if current_coverage is None:
        return EPSILON

    if current_coverage < COVERAGE_THRESHOLD:
        eps = EPSILON_LOW
    else:
        eps = EPSILON_HIGH

    # Clamp values
    eps = max(MIN_EPSILON, min(MAX_EPSILON, eps))
    return eps


def select_mode(current_coverage=None):
    """
    Epsilon-greedy selection
    Returns: "ml" or "random"
    """

    eps = get_epsilon(current_coverage)

    if random.random() < eps:
        mode = "random"
    else:
        mode = "ml"

    if DEBUG_PRINT:
        print(f"[HYBRID] epsilon={eps:.3f}, mode={mode}")

    return mode