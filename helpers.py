import numpy as np
import pandas as pd

from config import MAX_POINTS_PER_TRACE, MAX_POINTS_PER_TRACE_ZOOM


def get_display_mode(zoom_percent: float) -> tuple[str, int]:
    """
    Normal view: lines
    Zoomed view: lines + markers
    """
    if zoom_percent < 20:
        return "lines", 0
    if zoom_percent < 60:
        return "lines+markers", 3
    return "lines+markers", 4


def get_target_points(zoom_percent: float) -> int:
    if zoom_percent < 20:
        return MAX_POINTS_PER_TRACE
    return MAX_POINTS_PER_TRACE_ZOOM


def downsample_xy(x_series: pd.Series, y_series: pd.Series, n_max: int):
    n = len(x_series)
    if n <= n_max:
        return x_series, y_series

    step = max(1, n // n_max)
    idx = x_series.index[::step]
    return x_series.loc[idx], y_series.loc[idx]


def compute_section_ranges(df: pd.DataFrame, selected_sections: list[str]) -> list[dict]:
    if "_section_in" not in df.columns:
        return []

    ranges = []
    for sec in sorted(selected_sections, key=float):
        mask = df["_section_in"] == float(sec)
        idx = df.index[mask]
        if len(idx) == 0:
            continue

        ranges.append(
            {
                "label": f'{sec}"',
                "t_min": idx.min(),
                "t_max": idx.max(),
            }
        )

    ranges.sort(key=lambda r: r["t_min"])
    return ranges


def normalize_series(s: pd.Series):
    s = pd.to_numeric(s, errors="coerce")
    s_valid = s.dropna()

    if s_valid.empty:
        return s * np.nan, np.nan, np.nan

    s_min = float(s_valid.min())
    s_max = float(s_valid.max())

    if np.isclose(s_min, s_max):
        return pd.Series(np.full(len(s), 0.5), index=s.index), s_min, s_max

    return (s - s_min) / (s_max - s_min), s_min, s_max


def format_number(value: float) -> str:
    if pd.isna(value):
        return "NA"
    if abs(value) >= 1000:
        return f"{value:,.0f}"
    if abs(value) >= 10:
        return f"{value:.1f}"
    return f"{value:.2f}"


def axis_annotation_y(param_idx: int) -> float:
    return -0.09 - (param_idx * 0.05)