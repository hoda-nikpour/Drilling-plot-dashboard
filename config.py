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

# Only these labels will appear in the user choice list.
# Aliases cover both the old logs and the new logs.
PARAMETER_ALIASES = {
    "Bit Depth": [
        "BDTI",          # new logs
        "BITD",
        "BIT_DEPTH"
    ],
    "Well Depth (DBTM)": [
        "GS_DBTM",       # old logs
        "DBTM"           # old + new logs
    ],
    "BPOS": [
        "GS_BPOS",       # old logs
        "BPOS"           # old + new logs
    ],
    "HKL": [
        "GS_HKLD",       # old logs
        "HKL",
        "HKLD"
    ],
    "MFI": [
        "GS_MFI",        # in case present in some old files
        "MFI"            # new logs
    ],
    "SPP": [
        "GS_SPPA",       # old logs
        "SPP",           # new logs
        "SPPA"           # old logs
    ],
    "RPMB": [
        "RPMB",          # new logs
        "GS_RPM",        # old logs
        "RPM"            # old logs
    ],
    "TRQ": [
        "GS_TQA",        # old logs
        "TRQ",           # new logs
        "TQA"            # old logs
    ],
    "Pit Level": [
        "GS_PITLV",
        "GS_PITLVL",
        "GS_PIT",
        "PITLV",
        "PITLVL",
        "PIT"
    ],
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

# Logical plotting ranges used to mimic the figure style.
# If a parameter is missing here, the dashboard falls back to data min/max.
LOGICAL_PARAMETER_RANGES = {
    "Bit Depth": (0.0, 6000.0),
    "Well Depth (DBTM)": (0.0, 6000.0),
    "BPOS": (0.0, 50.0),
    "HKL": (0.0, 250.0),
    "MFI": (0.0, 4000.0),
    "SPP": (-200.0, 4000.0),
    "RPMB": (-100.0, 250.0),
    "TRQ": (-20.0, 40.0),
    "Pit Level": (0.0, 100.0),
}

AGENT_TRACK_XRANGE = (0.0, 1.0)