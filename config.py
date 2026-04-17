# from pathlib import Path

# BASE_DIR = Path(__file__).parent
# DATA_DIR = BASE_DIR / "data"

# # Dashboard settings
# N_TRACKS = 4
# MAX_PARAMS_PER_TRACK = 3

# # Performance tuning
# MAX_POINTS_PER_TRACE = 3000
# MAX_POINTS_PER_TRACE_ZOOM = 6000

# # Metadata columns required for the app
# REQUIRED_META_COLUMNS = ["TIME", "_section_in", "DEPT"]

# # Track colors
# TRACK_COLOR_PALETTE = [
#     "#8E44AD",  # purple
#     "#3498DB",  # blue
#     "#E74C3C",  # red
# ]

# # Only these labels will appear in the user choice list.
# # Aliases cover both the old logs and the new logs.
# PARAMETER_ALIASES = {
#     "Bit Depth": [
#         "BDTI",          # new logs
#         "BITD",
#         "BIT_DEPTH"
#     ],
#     "Well Depth (DBTM)": [
#         "GS_DBTM",       # old logs
#         "DBTM"           # old + new logs
#     ],
#     "BPOS": [
#         "GS_BPOS",       # old logs
#         "BPOS"           # old + new logs
#     ],
#     "HKL": [
#         "GS_HKLD",       # old logs
#         "HKL",
#         "HKLD"
#     ],
#     "MFI": [
#         "GS_MFI",        # in case present in some old files
#         "MFI"            # new logs
#     ],
#     "SPP": [
#         "GS_SPPA",       # old logs
#         "SPP",           # new logs
#         "SPPA"           # old logs
#     ],
#     "RPMB": [
#         "RPMB",          # new logs
#         "GS_RPM",        # old logs
#         "RPM"            # old logs
#     ],
#     "TRQ": [
#         "GS_TQA",        # old logs
#         "TRQ",           # new logs
#         "TQA"            # old logs
#     ],
#     "Pit Level": [
#         "GS_PITLV",
#         "GS_PITLVL",
#         "GS_PIT",
#         "PITLV",
#         "PITLVL",
#         "PIT"
#     ],
# }

# PARAMETER_DISPLAY_NAMES = {
#     "Bit Depth": "Bit Depth — current bit depth",
#     "Well Depth (DBTM)": "DBTM — well depth / depth to bottom",
#     "BPOS": "BPOS — block position",
#     "HKL": "HKL — hook load",
#     "MFI": "MFI — mud flow in",
#     "SPP": "SPP — standpipe pressure",
#     "RPMB": "RPMB — rotary speed",
#     "TRQ": "TRQ — torque",
#     "Pit Level": "Pit Level — mud pit level",
# }

# # Logical plotting ranges used to mimic the figure style.
# # If a parameter is missing here, the dashboard falls back to data min/max.
# LOGICAL_PARAMETER_RANGES = {
#     "Bit Depth": (0.0, 6000.0),
#     "Well Depth (DBTM)": (0.0, 6000.0),
#     "BPOS": (0.0, 50.0),
#     "HKL": (0.0, 250.0),
#     "MFI": (0.0, 4000.0),
#     "SPP": (-200.0, 4000.0),
#     "RPMB": (-100.0, 250.0),
#     "TRQ": (-20.0, 40.0),
#     "Pit Level": (0.0, 100.0),
# }

# AGENT_TRACK_XRANGE = (0.0, 1.0)


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




# # # Confirmed aliases found in the provided Volve and/or Gullfaks logs.
# # # Labeling convention in comments:
# # #   [V] = present in Volve logs
# # #   [G] = present in Gullfaks logs
# # #   [V,G] = present in both

# # PARAMETER_ALIASES = {
# #     # --- Pal's requested parameters ---
# #     "Bit Depth": [
# #         "BDTI",          # [V,G]
# #         "BITD",          # common alias, not seen in pasted logs
# #         "BIT_DEPTH"      # common alias, not seen in pasted logs
# #     ],
# #     "Well Depth (DBTM)": [
# #         "GS_DBTM",       # [V]
# #         "DBTM"           # [V,G]
# #     ],
# #     "BPOS": [
# #         "GS_BPOS",       # [V]
# #         "BPOS"           # [V,G]
# #     ],
# #     "HKL": [
# #         "GS_HKLD",       # [V]
# #         "HKL",           # [G]
# #         "HKLD",          # [V]
# #         "HKLX",          # [V]
# #         "HKLI"           # [V]
# #     ],
# #     "MFI": [
# #         "MFI"            # [G]
# #     ],
# #     "SPP": [
# #         "GS_SPPA",       # [V]
# #         "SPP",           # [G]
# #         "SPPA",          # [V]
# #         "SIG_SPP5s"      # [V]
# #     ],
# #     "RPMB": [
# #         "RPMB",          # [G]
# #         "GS_RPM",        # [V]
# #         "RPM",           # [V]
# #         "RPM30s",        # [V]
# #         "DRPM",          # [V]
# #         "DRPM30s",       # [V]
# #         "NRPM_RT",       # [V]
# #         "TRPM",          # [V]
# #         "TRPM_RT"        # [V]
# #     ],
# #     "TRQ": [
# #         "GS_TQA",        # [V]
# #         "TRQ",           # [G]
# #         "TQA",           # [V]
# #         "SIG_TQ30s"      # [V]
# #     ],

# #     # Pit Level not confirmed in pasted logs; keep as candidate aliases only
# #     "Pit Level": [
# #         "GS_PITLV",      # candidate, not seen in pasted logs
# #         "GS_PITLVL",     # candidate, not seen in pasted logs
# #         "GS_PIT",        # candidate, not seen in pasted logs
# #         "PITLV",         # candidate, not seen in pasted logs
# #         "PITLVL",        # candidate, not seen in pasted logs
# #         "PIT"            # candidate, not seen in pasted logs
# #     ],

# #     # --- Other well-known drilling parameters clearly present in the logs ---
# #     "WOB": [
# #         "WOB",           # [G]
# #         "SWOB",          # [V]
# #         "SWOB30s",       # [V]
# #         "GS_SWOB"        # [V]
# #     ],
# #     "ROP": [
# #         "ROP",           # [V,G]
# #         "ROP5",          # [V]
# #         "ROP30s",        # [V]
# #         "GS_ROP",        # [V]
# #         "QROP"           # [V]
# #     ],
# #     "Flow Rate": [
# #         "TFLO",          # [V]
# #         "GS_TFLO",       # [V]
# #         "TFLO30s",       # [V]
# #         "MFI",           # [G] mud flow in
# #         "MFO"            # [G] mud flow out
# #     ],
# #     "SPM": [
# #         "SPM1",          # [V]
# #         "SPM2",          # [V]
# #         "SPM3",          # [V]
# #         "SPM4",          # [V]
# #         "GS_SPM1",       # [V]
# #         "GS_SPM2",       # [V]
# #         "GS_SPM3",       # [V]
# #         "SPM"            # common alias, not seen in pasted logs
# #     ],
# #     "ECD": [
# #         "ECD_ECO_RT",    # [V]
# #         "ECD_MW_IN",     # [V]
# #         "ECD_P",         # [V]
# #         "ECDB",          # [G]
# #         "ECDC",          # [G]
# #         "ECDM",          # [G]
# #         "ECDT",          # [G]
# #         "ECDW"           # [G]
# #     ],
# #     "Inclination": [
# #         "INCL_CONT_RT",  # [V]
# #         "SRVINC"         # [V]
# #     ],
# #     "Azimuth": [
# #         "AZIM_CONT_RT",  # [V]
# #         "SRVAZI"         # [V]
# #     ],
# #     "TVD": [
# #         "TVDE",          # [V]
# #         "SRVTVD"         # [V]
# #     ],
# #     "Mud Weight": [
# #         "MWTI",          # [V]
# #         "MWIN",          # [V]
# #         "GS_MWTI",       # [V]
# #         "MWDA",          # [G]
# #         "MWDP",          # [G]
# #         "MWDT"           # [G]
# #     ],
# #     "Gas": [
# #         "GAS",           # [G]
# #         "GS_GASA",       # [V]
# #         "GS_G_C1",       # [V]
# #         "GS_G_C2",       # [V]
# #         "GS_G_C3",       # [V]
# #         "GS_G_NC4",      # [V]
# #         "GS_G_NC5"       # [V]
# #     ],
# #     "Temperature": [
# #         "GTEMP",         # [V]
# #         "TEMP_DNI_RT"    # [V]
# #     ],
# #     "Block Velocity": [
# #         "BVEL",          # [V]
# #         "BACC"           # [V]
# #     ],
# #     "Hole Depth / Measured Depth": [
# #         "DEPT",          # [V]
# #         "DMEA",          # [V]
# #         "GS_DMEA",       # [V]
# #         "DBTV",          # [V]
# #         "DVER"           # [V,G]
# #     ],
# #     "Pump Pressure / Choke / Annulus Pressure": [
# #         "APRS_P",        # [V]
# #         "BP_CORR_P",     # [V]
# #         "HYDR_RET_P",    # [V]
# #         "CEPP",          # [G]
# #         "CHP",           # [G]
# #         "COPP"           # [G]
# #     ],
# #     "Hookload / hoisting state indicators": [
# #         "HKLO",          # [V]
# #         "HKLN",          # [V]
# #         "HKLD30s",       # [V]
# #         "THKD"           # [V]
# #     ],
# #     "Bit / Rotary related": [
# #         "BITA",          # [G]
# #         "BITI",          # [G]
# #         "BITRUN",        # [V]
# #         "BROT",          # [G]
# #         "CRPM_RT"        # [V]
# #     ],
# #     "Mud Volume / Pit / Tank related": [
# #         "TTV2",          # [V]
# #         "GS_TTV1",       # [V]
# #         "TVA",           # [G]
# #         "GS_TVA",        # [V]
# #         "HVM",           # [V]
# #         "HVMX"           # [G]
# #     ],
# #     "Shock / Vibration": [
# #         "SHKLV",         # [V]
# #         "SHKTOT_RT",     # [V]
# #         "SHKPK_RT",      # [V]
# #         "SHK3TM_RT",     # [V]
# #         "SHKRATE_RT",    # [V]
# #         "SHKRSK_RT",     # [V]
# #         "SHKRSK_P",      # [V]
# #         "SHKL_DH_ECO_RT",# [V]
# #         "VIBX_RT",       # [V]
# #         "VIBLAT_RT"      # [V]
# #     ],
# #     "Stick Slip": [
# #         "Stick_RT",      # [V]
# #         "STK1",          # [V]
# #         "STK2",          # [V]
# #         "STK3",          # [V]
# #         "STK4",          # [V]
# #         "STKSLP",        # [V]
# #         "TSTK"           # [V]
# #     ]
# # }


# # PARAMETER_DISPLAY_NAMES = {
# #     # Requested by Pal
# #     "Bit Depth": "Bit Depth — current bit depth",
# #     "Well Depth (DBTM)": "DBTM — well depth / depth to bottom",
# #     "BPOS": "BPOS — block position",
# #     "HKL": "HKL — hook load",
# #     "MFI": "MFI — mud flow in",
# #     "SPP": "SPP — standpipe pressure",
# #     "RPMB": "RPMB — rotary speed",
# #     "TRQ": "TRQ — torque",
# #     "Pit Level": "Pit Level — mud pit level",

# #     # Other well-known parameters
# #     "WOB": "WOB — weight on bit",
# #     "ROP": "ROP — rate of penetration",
# #     "Flow Rate": "Flow Rate — mud flow rate",
# #     "SPM": "SPM — pump strokes per minute",
# #     "ECD": "ECD — equivalent circulating density",
# #     "Inclination": "Inclination — well angle",
# #     "Azimuth": "Azimuth — well direction",
# #     "TVD": "TVD — true vertical depth",
# #     "Mud Weight": "Mud Weight — drilling fluid density",
# #     "Gas": "Gas — gas / hydrocarbon readings",
# #     "Temperature": "Temperature — downhole or surface temperature",
# #     "Block Velocity": "Block Velocity — traveling block speed / acceleration",
# #     "Hole Depth / Measured Depth": "Hole Depth / Measured Depth — measured/vertical/reference depth channels",
# #     "Pump Pressure / Choke / Annulus Pressure": "Pressure — pump / annulus / choke related pressure channels",
# #     "Hookload / hoisting state indicators": "Hookload indicators — hookload state and derived channels",
# #     "Bit / Rotary related": "Bit / Rotary related — bit state and rotary indicators",
# #     "Mud Volume / Pit / Tank related": "Mud Volume / Tank related — tank/volume level channels",
# #     "Shock / Vibration": "Shock / Vibration — vibration and shock indicators",
# #     "Stick Slip": "Stick Slip — torsional vibration / stick-slip indicators",
# # }


# # # Logical plotting ranges. These are practical defaults, not strict physics.
# # LOGICAL_PARAMETER_RANGES = {
# #     "Bit Depth": (0.0, 7000.0),
# #     "Well Depth (DBTM)": (0.0, 7000.0),
# #     "BPOS": (0.0, 50.0),
# #     "HKL": (0.0, 300.0),
# #     "MFI": (0.0, 5000.0),
# #     "SPP": (-200.0, 5000.0),
# #     "RPMB": (-100.0, 300.0),
# #     "TRQ": (-20.0, 60.0),
# #     "Pit Level": (0.0, 100.0),

# #     "WOB": (0.0, 100.0),
# #     "ROP": (0.0, 100.0),
# #     "Flow Rate": (0.0, 5000.0),
# #     "SPM": (0.0, 200.0),
# #     "ECD": (0.0, 3.0),
# #     "Inclination": (0.0, 90.0),
# #     "Azimuth": (0.0, 360.0),
# #     "TVD": (0.0, 7000.0),
# #     "Mud Weight": (0.0, 3.0),
# #     "Gas": (0.0, 1000.0),
# #     "Temperature": (0.0, 250.0),
# #     "Block Velocity": (-5.0, 5.0),
# #     "Hole Depth / Measured Depth": (0.0, 7000.0),
# #     "Pump Pressure / Choke / Annulus Pressure": (0.0, 10000.0),
# #     "Hookload / hoisting state indicators": (0.0, 300.0),
# #     "Bit / Rotary related": (0.0, 500.0),
# #     "Mud Volume / Pit / Tank related": (0.0, 1000.0),
# #     "Shock / Vibration": (0.0, 100.0),
# #     "Stick Slip": (0.0, 100.0),
# # }

# # PARAMETER_SOURCE_COVERAGE = {
# #     "Bit Depth": ["Volve", "Gullfaks"],
# #     "Well Depth (DBTM)": ["Volve", "Gullfaks"],
# #     "BPOS": ["Volve", "Gullfaks"],
# #     "HKL": ["Volve", "Gullfaks"],
# #     "MFI": ["Gullfaks"],
# #     "SPP": ["Volve", "Gullfaks"],
# #     "RPMB": ["Volve", "Gullfaks"],
# #     "TRQ": ["Volve", "Gullfaks"],
# #     "Pit Level": [],  # not confirmed in the pasted logs
# #     "WOB": ["Volve", "Gullfaks"],
# #     "ROP": ["Volve", "Gullfaks"],
# #     "Flow Rate": ["Volve", "Gullfaks"],
# #     "SPM": ["Volve"],
# #     "ECD": ["Volve", "Gullfaks"],
# #     "Inclination": ["Volve"],
# #     "Azimuth": ["Volve"],
# #     "TVD": ["Volve"],
# #     "Mud Weight": ["Volve", "Gullfaks"],
# #     "Gas": ["Volve", "Gullfaks"],
# #     "Temperature": ["Volve"],
# #     "Block Velocity": ["Volve"],
# #     "Hole Depth / Measured Depth": ["Volve", "Gullfaks"],
# #     "Pump Pressure / Choke / Annulus Pressure": ["Volve", "Gullfaks"],
# #     "Hookload / hoisting state indicators": ["Volve"],
# #     "Bit / Rotary related": ["Volve", "Gullfaks"],
# #     "Mud Volume / Pit / Tank related": ["Volve", "Gullfaks"],
# #     "Shock / Vibration": ["Volve"],
# #     "Stick Slip": ["Volve"],
# # }