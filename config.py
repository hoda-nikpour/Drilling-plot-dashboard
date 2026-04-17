from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

# Dashboard settings
N_TRACKS = 4
MAX_PARAMS_PER_TRACK = 3

# Performance tuning
MAX_POINTS_PER_TRACE = 3000
MAX_POINTS_PER_TRACE_ZOOM = 6000

# Metadata columns required for the app
REQUIRED_META_COLUMNS = ["TIME", "_section_in", "DEPT"]

# Track colors
TRACK_COLOR_PALETTE = [
    "#8E44AD",  # purple
    "#3498DB",  # blue
    "#E74C3C",  # red
]

# Sidebar labels mapped to possible raw data-file column names
PARAMETER_ALIASES = {
    "Bit Depth": ["BDTI", "BITD", "BIT_DEPTH"],
    "Well Depth (DBTM)": ["GS_DBTM", "DBTM"],
    "BPOS": ["GS_BPOS", "BPOS"],
    "HKL": ["GS_HKLD", "HKL", "HKLD"],
    "MFI": ["GS_MFI", "MFI"],
    "SPP": ["GS_SPPA", "SPP", "SPPA"],
    "RPMB": ["RPMB", "GS_RPM", "RPM"],
    "TRQ": ["GS_TQA", "TRQ", "TQA"],
    "Pit Level": ["GS_PITLV", "GS_PITLVL", "GS_PIT", "PITLV", "PITLVL", "PIT"],
}

PARAMETER_DISPLAY_NAMES = {
    "Bit Depth": "Bit Depth — current bit depth",
    "Well Depth (DBTM)": "DBTM — well depth / depth to bottom",
    "BPOS": "BPOS — block position",
    "HKL": "HKL — hook load",
    "MFI": "MFI — mud flow in",
    "SPP": "SPP — standpipe pressure",
    "RPMB": "RPMB — rotary speed",
    "TRQ": "TRQ — torque",
    "Pit Level": "Pit Level — mud pit level",
}

# Parameter catalog for boss review
PARAMETER_CATALOG = {
    "Bit Depth": {
        "meaning": "Current bit depth",
        "unit": "m",
        "logical_min": 0.0,
        "logical_max": 6000.0,
    },
    "Well Depth (DBTM)": {
        "meaning": "Well depth / depth to bottom",
        "unit": "m",
        "logical_min": 0.0,
        "logical_max": 6000.0,
    },
    "BPOS": {
        "meaning": "Block position",
        "unit": "m",
        "logical_min": 0.0,
        "logical_max": 50.0,
    },
    "HKL": {
        "meaning": "Hook load",
        "unit": "t or kkgf",
        "logical_min": 0.0,
        "logical_max": 250.0,
    },
    "MFI": {
        "meaning": "Mud flow in",
        "unit": "flow unit",
        "logical_min": 0.0,
        "logical_max": 4000.0,
    },
    "SPP": {
        "meaning": "Standpipe pressure",
        "unit": "kPa",
        "logical_min": -200.0,
        "logical_max": 4000.0,
    },
    "RPMB": {
        "meaning": "Rotary speed",
        "unit": "rpm",
        "logical_min": -100.0,
        "logical_max": 250.0,
    },
    "TRQ": {
        "meaning": "Torque",
        "unit": "kN.m",
        "logical_min": -20.0,
        "logical_max": 40.0,
    },
    "Pit Level": {
        "meaning": "Mud pit level",
        "unit": "level / volume unit",
        "logical_min": 0.0,
        "logical_max": 100.0,
    },
}

LOGICAL_PARAMETER_RANGES = {
    label: (meta["logical_min"], meta["logical_max"])
    for label, meta in PARAMETER_CATALOG.items()
}

AGENT_TRACK_XRANGE = (0.0, 1.0)