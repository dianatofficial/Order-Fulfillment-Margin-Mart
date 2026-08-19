import os
from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'
SQL_DIR = PROJECT_ROOT / 'src' / 'sql'

# Database Configuration
DUCKDB_PATH = DATA_DIR / 'warehouse.duckdb'

# Ensure base directories exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Business Rule Thresholds
DEFAULT_SLA_DAYS_BUFFER = 0.5
MAX_DISPATCH_LATENCY_HOURS_TARGET = 24.0
TARGET_GROSS_MARGIN_PCT = 35.0
LOW_MARGIN_ALERT_PCT = 15.0

# Simulation Parameters
DEFAULT_SAMPLE_ORDER_COUNT = 25000
RANDOM_SEED = 42
