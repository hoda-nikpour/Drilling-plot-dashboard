from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

# Dashboard settings
N_TRACKS = 4
MAX_PARAMS_PER_TRACK = 3

# Performance tuning
MAX_POINTS_PER_TRACE = 12000
MAX_POINTS_PER_TRACE_ZOOM = 20000

# Marker settings
# Important:
# Plotly zoom inside the chart does not automatically re-run Streamlit code,
# so marker size should not rely on chart zoom alone.
BASE_MARKER_SIZE = 1.2
ZOOM_MARKER_SIZE = 4.5

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
    # Pål observed that DBTM/GS_DBTM behaves like bit depth in the current data.
    "Bit Depth": ["GS_DBTM", "DBTM", "BDTI", "BITD", "BIT_DEPTH"],

    # True well/measured depth is likely hidden in these channels.
    "Well Depth": ["DEPT", "GS_DMEA", "DMEA", "DVER", "GS_DVER", "DBTV"],

    "BPOS": ["GS_BPOS", "BPOS"],
    "HKL": ["GS_HKLD", "HKL", "HKLD", "HKLX", "HKLI"],
    "WOB": ["WOB", "SWOB", "SWOB30s", "GS_SWOB"],
    "MFI": ["GS_MFI", "MFI", "GS_TFLO", "TFLO", "TFLO30s"],
    "SPP": ["GS_SPPA", "SPP", "SPPA", "SIG_SPP5s"],
    "RPMB": ["RPMB", "GS_RPM", "RPM", "RPM30s", "DRPM", "DRPM30s", "NRPM_RT", "TRPM", "TRPM_RT"],
    "TRQ": ["GS_TQA", "TRQ", "TQA", "SIG_TQ30s"],
    "ROP": ["ROP", "ROP5", "ROP30s", "GS_ROP", "QROP", "DRILL_RATE", "RATE_OF_PENETRATION"],
    "Pit Level": ["GS_PITLV", "GS_PITLVL", "GS_PIT", "PITLV", "PITLVL", "PIT", "TVA", "GS_TVA", "HVM", "HVMX"],
}

PARAMETER_DISPLAY_NAMES = {
    "Bit Depth": "Bit Depth — bit/depth-to-bottom channel",
    "Well Depth": "Well Depth — measured/reference well depth",
    "BPOS": "BPOS — block position",
    "HKL": "HKL — hook load",
    "WOB": "WOB — weight on bit",
    "MFI": "MFI — mud flow in",
    "SPP": "SPP — standpipe pressure",
    "RPMB": "RPMB — rotary speed",
    "TRQ": "TRQ — torque",
    "ROP": "ROP — rate of penetration",
    "Pit Level": "Pit Level — mud pit level",
}

PARAMETER_CATALOG = {
    "Bit Depth": {
        "meaning": "Bit depth / depth-to-bottom channel",
        "unit": "m",
        "logical_min": 0.0,
        "logical_max": 6000.0,
    },
    "Well Depth": {
        "meaning": "Measured/reference well depth",
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
    "WOB": {
        "meaning": "Weight on bit",
        "unit": "t or kkgf",
        "logical_min": 0.0,
        "logical_max": 100.0,
    },
    "MFI": {
        "meaning": "Mud flow in",
        "unit": "l/min",
        "logical_min": 0.0,
        "logical_max": 4000.0,
    },
    "SPP": {
        "meaning": "Standpipe pressure",
        "unit": "kPa",
        "logical_min": 0.0,
        "logical_max": 4000.0,
    },
    "RPMB": {
        "meaning": "Rotary speed",
        "unit": "rpm",
        "logical_min": 0.0,
        "logical_max": 250.0,
    },
    "TRQ": {
        "meaning": "Torque",
        "unit": "kN.m",
        "logical_min": 0.0,
        "logical_max": 40.0,
    },
    "ROP": {
        "meaning": "Rate of penetration",
        "unit": "m/h",
        "logical_min": 0.0,
        "logical_max": 200.0,
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