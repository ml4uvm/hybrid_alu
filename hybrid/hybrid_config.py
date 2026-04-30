# Hybrid ML Configuration

# --- Core exploration parameter ---
# Probability of choosing RANDOM instead of ML
EPSILON = 0.03   # start low for ALU sanity

# --- Dynamic epsilon control (optional) ---
USE_DYNAMIC_EPSILON = False

# Coverage-based switching (used only if dynamic enabled)
# Increase exploration when nearing saturation
COVERAGE_THRESHOLD = 120   # for ALU (out of 128 bins)

EPSILON_LOW = 0.02   # early phase (trust ML)
EPSILON_HIGH = 0.1   # late phase (more exploration)

# --- Safety limits ---
MIN_EPSILON = 0.01
MAX_EPSILON = 0.3

# --- Execution control ---
MAX_TESTS = 500   # fallback stop condition

# --- Debug / logging ---
LOG_MODE_ENABLED = True   # log whether ML or RANDOM was used
DEBUG_PRINT = False       # enable for tracing decisions