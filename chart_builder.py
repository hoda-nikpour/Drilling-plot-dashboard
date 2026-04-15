import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from config import AGENT_TRACK_XRANGE, LOGICAL_PARAMETER_RANGES, N_TRACKS
from helpers import downsample_xy, format_number, get_display_mode, get_target_points


def add_section_boundaries(fig: go.Figure, section_ranges: list[dict], t_min_view, t_max_view):
    if not section_ranges or t_min_view is None or t_max_view is None:
        return

    total_ns = float((t_max_view - t_min_view).value)
    if total_ns <= 0:
        return

    def to_paper_y(t):
        frac = float((t - t_min_view).value) / total_ns
        return 1.0 - max(0.0, min(1.0, frac))

    for i, sr in enumerate(section_ranges):
        if i > 0:
            y_line = to_paper_y(sr["t_min"])
            if 0.01 < y_line < 0.99:
                fig.add_shape(
                    type="line",
                    x0=0, x1=1, xref="paper",
                    y0=y_line, y1=y_line, yref="paper",
                    line=dict(dash="dash", color="rgba(70,70,70,0.30)", width=1),
                )

        mid = sr["t_min"] + (sr["t_max"] - sr["t_min"]) / 2
        y_mid = max(0.02, min(0.98, to_paper_y(mid)))

        fig.add_annotation(
            xref="paper",
            yref="paper",
            x=0.006,
            y=y_mid,
            text=sr["label"],
            textangle=-90,
            showarrow=False,
            font=dict(size=9, color="#333"),
            bgcolor="rgba(255,255,255,0.65)",
            borderpad=2,
            xanchor="center",
            yanchor="middle",
        )


def _normalize_with_range(series: pd.Series, label: str):
    s = pd.to_numeric(series, errors="coerce")
    s_valid = s.dropna()
    if s_valid.empty:
        return s * np.nan, np.nan, np.nan

    range_min, range_max = LOGICAL_PARAMETER_RANGES.get(
        label,
        (float(s_valid.min()), float(s_valid.max()))
    )

    if np.isclose(range_min, range_max):
        return pd.Series(np.full(len(s), 0.5), index=s.index), range_min, range_max

    s_clipped = s.clip(lower=range_min, upper=range_max)
    s_norm = (s_clipped - range_min) / (range_max - range_min)
    return s_norm, range_min, range_max


def _scale_annotation_y(param_idx: int) -> float:
    return -0.09 - (param_idx * 0.05)


def _agent_line_width(severity: str) -> int:
    return {"Low": 2, "Medium": 5, "High": 8}.get(severity, 5)


def add_agent_track(fig: go.Figure, agent_cfg: dict, row: int, col: int):
    # Tagged area
    if agent_cfg.get("enable_tag"):
        fig.add_shape(
            type="rect",
            xref="x4",
            yref="y",
            x0=0.12,
            x1=0.48,
            y0=agent_cfg["tag_start"],
            y1=agent_cfg["tag_end"],
            fillcolor="rgba(128, 0, 128, 0.18)",
            line=dict(color="rgba(128, 0, 128, 0.75)", width=1),
        )
        fig.add_annotation(
            xref="x4",
            yref="paper",
            x=0.30,
            y=-0.09,
            text="<span style='color:#8E44AD'><b>Tagged area</b></span>",
            showarrow=False,
            font=dict(size=10),
        )

    # Resulting data agent
    if agent_cfg.get("enable_agent"):
        width = _agent_line_width(agent_cfg.get("severity", "Medium"))
        y_vals = pd.date_range(agent_cfg["agent_start"], agent_cfg["agent_end"], periods=20)
        x_vals = np.full(len(y_vals), 0.76)

        fig.add_trace(
            go.Scatter(
                x=x_vals,
                y=y_vals,
                mode="lines",
                line=dict(color="#E74C3C", width=width),
                showlegend=False,
                hovertemplate="Data Agent Result<extra></extra>",
            ),
            row=row,
            col=col,
        )

        fig.add_annotation(
            xref="x4",
            yref="paper",
            x=0.76,
            y=-0.14,
            text=f"<span style='color:#E74C3C'><b>Agent result</b> — {agent_cfg.get('severity', 'Medium')}</span>",
            showarrow=False,
            font=dict(size=10),
        )

    fig.update_xaxes(
        row=row,
        col=col,
        range=list(AGENT_TRACK_XRANGE),
        showgrid=True,
        gridcolor="rgba(140,140,140,0.20)",
        gridwidth=0.6,
        zeroline=False,
        showticklabels=False,
        side="top",
        tickmode="array",
        tickvals=[i / 20 for i in range(21)],
    )


def create_multi_track_chart(
    df: pd.DataFrame,
    track_params: list[list[str]],
    track_param_labels: list[list[str]],
    track_colors: list[list[str]],
    zoom_percent: float,
    section_ranges: list[dict] | None = None,
    agent_cfg: dict | None = None,
) -> go.Figure:
    subplot_titles = ["Track 1", "Track 2", "Track 3", "Track 4"]

    fig = make_subplots(
        rows=1,
        cols=N_TRACKS,
        shared_yaxes=True,
        horizontal_spacing=0.02,
        subplot_titles=subplot_titles,
    )

    mode, marker_size = get_display_mode(zoom_percent)
    target_points = get_target_points(zoom_percent)

    t_min_view = df.index.min() if not df.empty else None
    t_max_view = df.index.max() if not df.empty else None

    # Tracks 1–3: drilling parameters
    for track_idx in range(3):
        params = track_params[track_idx]
        labels = track_param_labels[track_idx]
        colors = track_colors[track_idx]

        for param_idx, (col, label, color) in enumerate(zip(params, labels, colors)):
            if col not in df.columns:
                continue

            series = df[col]
            valid = series.notna()
            if not valid.any():
                continue

            raw_x = series.loc[valid]
            raw_y = pd.Series(raw_x.index, index=raw_x.index)

            x_norm_full, x_min, x_max = _normalize_with_range(raw_x, label)
            x_plot, y_plot = downsample_xy(x_norm_full, raw_y, target_points)

            if x_plot.dropna().empty:
                continue

            raw_vals = raw_x.loc[x_plot.index]

            hovertemplate = (
                f"<b>{label}</b><br>"
                "Value: %{customdata[0]:.3f}<br>"
                "Date: %{y|%Y-%m-%d}<br>"
                "Time: %{y|%H:%M:%S}<extra></extra>"
            )

            fig.add_trace(
                go.Scattergl(
                    x=x_plot.values,
                    y=y_plot.values,
                    mode=mode,
                    name=f"Track {track_idx + 1} - {label}",
                    showlegend=False,
                    line=dict(color=color, width=1.35),
                    marker=dict(size=marker_size, color=color),
                    customdata=np.column_stack([raw_vals.values]),
                    hovertemplate=hovertemplate,
                ),
                row=1,
                col=track_idx + 1,
            )

            xaxis_name = "x domain" if track_idx == 0 else f"x{track_idx + 1} domain"
            fig.add_annotation(
                xref=xaxis_name,
                yref="paper",
                x=0.5,
                y=_scale_annotation_y(param_idx),
                text=(
                    f"<span style='color:{color}'><b>{label}</b></span> "
                    f"<span style='color:{color}'>{format_number(x_min)}</span>"
                    f" &nbsp;&nbsp; "
                    f"<span style='color:{color}'>{format_number(x_max)}</span>"
                ),
                showarrow=False,
                align="center",
                font=dict(size=10),
            )

        fig.update_xaxes(
            row=1,
            col=track_idx + 1,
            range=[0, 1],
            showgrid=True,
            gridcolor="rgba(140,140,140,0.20)",
            gridwidth=0.6,
            zeroline=False,
            showticklabels=False,
            side="top",
            tickmode="array",
            tickvals=[i / 20 for i in range(21)],
        )

    # Track 4: data agents
    if agent_cfg:
        add_agent_track(fig, agent_cfg, row=1, col=4)

    if section_ranges and t_min_view is not None and t_max_view is not None:
        add_section_boundaries(fig, section_ranges, t_min_view, t_max_view)

    y_range = None
    if t_min_view is not None and t_max_view is not None:
        y_range = [t_max_view, t_min_view]

    fig.update_yaxes(
        # title_text="Date<br>Time",
        range=y_range,
        autorange=False if y_range else "reversed",
        showgrid=True,
        gridcolor="rgba(140,140,140,0.20)",
        gridwidth=0.6,
        tickformat="%d-%b-%y\n%H:%M:%S",
        nticks=24,
    )

    fig.update_layout(
        height=860,
        margin=dict(l=80, r=20, t=65, b=165),
        hovermode="closest",
        plot_bgcolor="white",
        paper_bgcolor="white",
        # title=dict(
        #     text="Selected Drilling Parameters and Data Agent Review",
        #     x=0.5,
        #     xanchor="center",
        #     font=dict(size=13, color="#1E3A5F"),
        # ),
        uirevision="keep_zoom_state",
    )

    return fig