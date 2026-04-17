# import numpy as np
# import pandas as pd
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots

# from config import AGENT_TRACK_XRANGE, LOGICAL_PARAMETER_RANGES, N_TRACKS
# from helpers import downsample_xy, format_number, get_display_mode, get_target_points


# TAG_X = 0.22
# OVERLAP_X = 0.50
# AGENT_X = 0.78


# def add_section_boundaries(fig: go.Figure, section_ranges: list[dict], t_min_view, t_max_view):
#     if not section_ranges or t_min_view is None or t_max_view is None:
#         return

#     total_ns = float((t_max_view - t_min_view).value)
#     if total_ns <= 0:
#         return

#     def to_paper_y(t):
#         frac = float((t - t_min_view).value) / total_ns
#         return 1.0 - max(0.0, min(1.0, frac))

#     for i, sr in enumerate(section_ranges):
#         if i > 0:
#             y_line = to_paper_y(sr["t_min"])
#             if 0.01 < y_line < 0.99:
#                 fig.add_shape(
#                     type="line",
#                     x0=0, x1=1, xref="paper",
#                     y0=y_line, y1=y_line, yref="paper",
#                     line=dict(dash="dash", color="rgba(70,70,70,0.30)", width=1),
#                 )

#         mid = sr["t_min"] + (sr["t_max"] - sr["t_min"]) / 2
#         y_mid = max(0.02, min(0.98, to_paper_y(mid)))

#         fig.add_annotation(
#             xref="paper",
#             yref="paper",
#             x=0.006,
#             y=y_mid,
#             text=sr["label"],
#             textangle=-90,
#             showarrow=False,
#             font=dict(size=9, color="#333"),
#             bgcolor="rgba(255,255,255,0.65)",
#             borderpad=2,
#             xanchor="center",
#             yanchor="middle",
#         )


# def _normalize_with_range(series: pd.Series, label: str):
#     s = pd.to_numeric(series, errors="coerce")
#     s_valid = s.dropna()
#     if s_valid.empty:
#         return s * np.nan, np.nan, np.nan

#     range_min, range_max = LOGICAL_PARAMETER_RANGES.get(
#         label,
#         (float(s_valid.min()), float(s_valid.max()))
#     )

#     if np.isclose(range_min, range_max):
#         return pd.Series(np.full(len(s), 0.5), index=s.index), range_min, range_max

#     s_clipped = s.clip(lower=range_min, upper=range_max)
#     s_norm = (s_clipped - range_min) / (range_max - range_min)
#     return s_norm, range_min, range_max


# def _scale_annotation_y(param_idx: int) -> float:
#     return -0.09 - (param_idx * 0.05)


# def _agent_line_width(severity: str) -> int:
#     return {"Low": 2, "Medium": 4, "High": 7}.get(severity, 4)


# def _interval_overlap(a_start, a_end, b_start, b_end):
#     start = max(pd.Timestamp(a_start), pd.Timestamp(b_start))
#     end = min(pd.Timestamp(a_end), pd.Timestamp(b_end))
#     if start < end:
#         return start, end
#     return None


# def _compute_overlap_intervals(tag_intervals: list[dict], agent_intervals: list[dict]) -> list[dict]:
#     overlaps = []
#     for tag in tag_intervals:
#         for agent in agent_intervals:
#             ov = _interval_overlap(tag["start"], tag["end"], agent["start"], agent["end"])
#             if ov is not None:
#                 overlaps.append(
#                     {
#                         "start": ov[0],
#                         "end": ov[1],
#                         "tag_label": tag.get("label", ""),
#                         "agent_label": agent.get("label", ""),
#                     }
#                 )
#     return overlaps


# def _add_vertical_interval_line(
#     fig: go.Figure,
#     x_pos: float,
#     start_time,
#     end_time,
#     color: str,
#     width: int,
#     row: int,
#     col: int,
#     hover_text: str | None = None,
# ):
#     y_vals = pd.date_range(pd.Timestamp(start_time), pd.Timestamp(end_time), periods=20)
#     x_vals = np.full(len(y_vals), x_pos)

#     fig.add_trace(
#         go.Scatter(
#             x=x_vals,
#             y=y_vals,
#             mode="lines",
#             line=dict(color=color, width=width),
#             showlegend=False,
#             hovertemplate=(hover_text or "") + "<extra></extra>",
#         ),
#         row=row,
#         col=col,
#     )


# def add_reference_line(fig: go.Figure, reference_time):
#     fig.add_shape(
#         type="line",
#         x0=0,
#         x1=1,
#         xref="paper",
#         y0=reference_time,
#         y1=reference_time,
#         yref="y",
#         line=dict(color="rgba(255,0,0,0.55)", width=2),
#     )


# def add_agent_track(fig: go.Figure, agent_cfg: dict, row: int, col: int):
#     tag_intervals = agent_cfg.get("tag_intervals", [])
#     agent_intervals = agent_cfg.get("agent_intervals", [])
#     overlap_intervals = _compute_overlap_intervals(tag_intervals, agent_intervals)

#     # subtle lane guides
#     for x_pos in [TAG_X, OVERLAP_X, AGENT_X]:
#         fig.add_shape(
#             type="line",
#             xref="x4",
#             yref="paper",
#             x0=x_pos,
#             x1=x_pos,
#             y0=0,
#             y1=1,
#             line=dict(color="rgba(100,100,100,0.18)", width=1, dash="dot"),
#         )

#     # tagger intervals: thin purple lane
#     for i, tag in enumerate(tag_intervals, start=1):
#         label = tag.get("label", f"Tag {i}")
#         hover_text = f"Tagger<br>{label}"
#         _add_vertical_interval_line(
#             fig=fig,
#             x_pos=TAG_X,
#             start_time=tag["start"],
#             end_time=tag["end"],
#             color="rgba(128, 0, 128, 0.85)",
#             width=5,
#             row=row,
#             col=col,
#             hover_text=hover_text,
#         )

#         mid_time = pd.Timestamp(tag["start"]) + (pd.Timestamp(tag["end"]) - pd.Timestamp(tag["start"])) / 2
#         fig.add_annotation(
#             xref="x4",
#             yref="y",
#             x=TAG_X - 0.05,
#             y=mid_time,
#             text=label,
#             showarrow=False,
#             font=dict(size=9, color="#6A0DAD"),
#             xanchor="right",
#             bgcolor="rgba(255,255,255,0.60)",
#         )

#     # overlap intervals: subtle green lane
#     for overlap in overlap_intervals:
#         hover_text = (
#             "Overlap<br>"
#             f"Tag: {overlap.get('tag_label', '')}<br>"
#             f"Agent: {overlap.get('agent_label', '')}"
#         )
#         _add_vertical_interval_line(
#             fig=fig,
#             x_pos=OVERLAP_X,
#             start_time=overlap["start"],
#             end_time=overlap["end"],
#             color="rgba(60, 160, 90, 0.90)",
#             width=6,
#             row=row,
#             col=col,
#             hover_text=hover_text,
#         )

#     # agent-hit intervals: thin red lane with thickness by severity
#     for i, agent in enumerate(agent_intervals, start=1):
#         label = agent.get("label", f"Hit {i}")
#         severity = agent.get("severity", "Medium")
#         hover_text = f"Agent hit<br>{label}<br>Severity: {severity}"
#         _add_vertical_interval_line(
#             fig=fig,
#             x_pos=AGENT_X,
#             start_time=agent["start"],
#             end_time=agent["end"],
#             color="rgba(220, 50, 47, 0.92)",
#             width=_agent_line_width(severity),
#             row=row,
#             col=col,
#             hover_text=hover_text,
#         )

#         mid_time = pd.Timestamp(agent["start"]) + (pd.Timestamp(agent["end"]) - pd.Timestamp(agent["start"])) / 2
#         fig.add_annotation(
#             xref="x4",
#             yref="y",
#             x=AGENT_X + 0.05,
#             y=mid_time,
#             text=label,
#             showarrow=False,
#             font=dict(size=9, color="#C0392B"),
#             xanchor="left",
#             bgcolor="rgba(255,255,255,0.60)",
#         )

#     # lane labels
#     fig.add_annotation(
#         xref="x4", yref="paper", x=TAG_X, y=1.03,
#         text="<b>Tagger</b>",
#         showarrow=False, font=dict(size=10, color="#6A0DAD")
#     )
#     fig.add_annotation(
#         xref="x4", yref="paper", x=OVERLAP_X, y=1.03,
#         text="<b>Overlap</b>",
#         showarrow=False, font=dict(size=10, color="#2E8B57")
#     )
#     fig.add_annotation(
#         xref="x4", yref="paper", x=AGENT_X, y=1.03,
#         text="<b>Agent</b>",
#         showarrow=False, font=dict(size=10, color="#C0392B")
#     )

#     summary = agent_cfg.get("summary", {})
#     summary_text = (
#         f"Tags: {summary.get('tag_count', 0)}"
#         f" &nbsp;|&nbsp; Hits: {summary.get('agent_count', 0)}"
#         f" &nbsp;|&nbsp; Overlap: {summary.get('overlap_count', 0)} / {summary.get('tag_count', 0)}"
#     )
#     fig.add_annotation(
#         xref="x4",
#         yref="paper",
#         x=0.5,
#         y=-0.09,
#         text=summary_text,
#         showarrow=False,
#         font=dict(size=10, color="#444"),
#     )

#     fig.update_xaxes(
#         row=row,
#         col=col,
#         range=list(AGENT_TRACK_XRANGE),
#         showgrid=False,
#         zeroline=False,
#         showticklabels=False,
#         side="top",
#         title_text="",
#     )


# def create_multi_track_chart(
#     df: pd.DataFrame,
#     track_params: list[list[str]],
#     track_param_labels: list[list[str]],
#     track_colors: list[list[str]],
#     zoom_percent: float,
#     section_ranges: list[dict] | None = None,
#     agent_cfg: dict | None = None,
#     chart_height: int = 860,
# ) -> go.Figure:
#     subplot_titles = ["Track 1", "Track 2", "Track 3", "Track 4"]

#     fig = make_subplots(
#         rows=1,
#         cols=N_TRACKS,
#         shared_yaxes=True,
#         horizontal_spacing=0.02,
#         subplot_titles=subplot_titles,
#     )

#     mode, marker_size = get_display_mode(zoom_percent)
#     target_points = get_target_points(zoom_percent)

#     t_min_view = df.index.min() if not df.empty else None
#     t_max_view = df.index.max() if not df.empty else None

#     for track_idx in range(3):
#         params = track_params[track_idx]
#         labels = track_param_labels[track_idx]
#         colors = track_colors[track_idx]

#         for param_idx, (col, label, color) in enumerate(zip(params, labels, colors)):
#             if col not in df.columns:
#                 continue

#             series = df[col]
#             valid = series.notna()
#             if not valid.any():
#                 continue

#             raw_x = series.loc[valid]
#             raw_y = pd.Series(raw_x.index, index=raw_x.index)

#             x_norm_full, x_min, x_max = _normalize_with_range(raw_x, label)
#             x_plot, y_plot = downsample_xy(x_norm_full, raw_y, target_points)

#             if x_plot.dropna().empty:
#                 continue

#             raw_vals = raw_x.loc[x_plot.index]

#             hovertemplate = (
#                 f"<b>{label}</b><br>"
#                 "Value: %{customdata[0]:.3f}<br>"
#                 "Date: %{y|%Y-%m-%d}<br>"
#                 "Time: %{y|%H:%M:%S}<extra></extra>"
#             )

#             fig.add_trace(
#                 go.Scattergl(
#                     x=x_plot.values,
#                     y=y_plot.values,
#                     mode=mode,
#                     name=f"Track {track_idx + 1} - {label}",
#                     showlegend=False,
#                     line=dict(color=color, width=1.35),
#                     marker=dict(size=marker_size, color=color),
#                     customdata=np.column_stack([raw_vals.values]),
#                     hovertemplate=hovertemplate,
#                 ),
#                 row=1,
#                 col=track_idx + 1,
#             )

#             xaxis_name = "x domain" if track_idx == 0 else f"x{track_idx + 1} domain"
#             fig.add_annotation(
#                 xref=xaxis_name,
#                 yref="paper",
#                 x=0.5,
#                 y=_scale_annotation_y(param_idx),
#                 text=(
#                     f"<span style='color:{color}'><b>{label}</b></span> "
#                     f"<span style='color:{color}'>{format_number(x_min)}</span>"
#                     f" &nbsp;&nbsp; "
#                     f"<span style='color:{color}'>{format_number(x_max)}</span>"
#                 ),
#                 showarrow=False,
#                 align="center",
#                 font=dict(size=10),
#             )

#         fig.update_xaxes(
#             row=1,
#             col=track_idx + 1,
#             range=[0, 1],
#             showgrid=True,
#             gridcolor="rgba(140,140,140,0.20)",
#             gridwidth=0.6,
#             zeroline=False,
#             showticklabels=False,
#             side="top",
#             tickmode="array",
#             tickvals=[i / 20 for i in range(21)],
#         )

#     if agent_cfg:
#         add_agent_track(fig, agent_cfg, row=1, col=4)

#     if section_ranges and t_min_view is not None and t_max_view is not None:
#         add_section_boundaries(fig, section_ranges, t_min_view, t_max_view)

#     if agent_cfg and agent_cfg.get("show_reference_line") and agent_cfg.get("reference_time") is not None:
#         add_reference_line(fig, agent_cfg["reference_time"])

#     y_range = None
#     if t_min_view is not None and t_max_view is not None:
#         y_range = [t_max_view, t_min_view]

#     fig.update_yaxes(
#         range=y_range,
#         autorange=False if y_range else "reversed",
#         showgrid=True,
#         gridcolor="rgba(140,140,140,0.20)",
#         gridwidth=0.6,
#         tickformat="%d-%b-%y\n%H:%M:%S",
#         nticks=24,
#     )

#     fig.update_layout(
#         height=chart_height,
#         margin=dict(l=80, r=20, t=75, b=165),
#         hovermode="closest",
#         plot_bgcolor="white",
#         paper_bgcolor="white",
#         uirevision="keep_zoom_state",
#     )

#     return fig

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from config import AGENT_TRACK_XRANGE, LOGICAL_PARAMETER_RANGES, N_TRACKS
from helpers import downsample_xy, format_number, get_display_mode, get_target_points


TAG_X = 0.24
OVERLAP_X = 0.50
AGENT_X = 0.76


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


def _agent_line_width(severity: str) -> int:
    return {"Low": 2, "Medium": 4, "High": 7}.get(severity, 4)


def _interval_overlap(a_start, a_end, b_start, b_end):
    start = max(pd.Timestamp(a_start), pd.Timestamp(b_start))
    end = min(pd.Timestamp(a_end), pd.Timestamp(b_end))
    if start < end:
        return start, end
    return None


def _compute_overlap_intervals(tag_intervals: list[dict], agent_intervals: list[dict]) -> list[dict]:
    overlaps = []
    for tag in tag_intervals:
        for agent in agent_intervals:
            ov = _interval_overlap(tag["start"], tag["end"], agent["start"], agent["end"])
            if ov is not None:
                overlaps.append(
                    {
                        "start": ov[0],
                        "end": ov[1],
                        "tag_label": tag.get("label", ""),
                        "agent_label": agent.get("label", ""),
                    }
                )
    return overlaps


def _build_dual_time_ticks(t_min_view, t_max_view, n_ticks: int = 12):
    if t_min_view is None or t_max_view is None:
        return None, None

    vals = pd.date_range(start=t_min_view, end=t_max_view, periods=n_ticks)
    texts = [
        f"{ts.strftime('%d-%b-%y')}&nbsp;&nbsp;&nbsp;{ts.strftime('%H:%M:%S')}"
        for ts in vals
    ]
    return vals, texts


def _add_vertical_interval_line(
    fig: go.Figure,
    x_pos: float,
    start_time,
    end_time,
    color: str,
    width: int,
    row: int,
    col: int,
    hover_text: str | None = None,
):
    y_vals = pd.date_range(pd.Timestamp(start_time), pd.Timestamp(end_time), periods=20)
    x_vals = np.full(len(y_vals), x_pos)

    fig.add_trace(
        go.Scatter(
            x=x_vals,
            y=y_vals,
            mode="lines",
            line=dict(color=color, width=width),
            showlegend=False,
            hovertemplate=(hover_text or "") + "<extra></extra>",
        ),
        row=row,
        col=col,
    )


def add_reference_line(fig: go.Figure, reference_time):
    fig.add_shape(
        type="line",
        x0=0,
        x1=1,
        xref="paper",
        y0=reference_time,
        y1=reference_time,
        yref="y",
        line=dict(color="rgba(255,0,0,0.55)", width=2),
    )


def add_agent_track(fig: go.Figure, agent_cfg: dict, row: int, col: int):
    tag_intervals = agent_cfg.get("tag_intervals", [])
    agent_intervals = agent_cfg.get("agent_intervals", [])
    overlap_intervals = _compute_overlap_intervals(tag_intervals, agent_intervals)

    for x_pos in [TAG_X, OVERLAP_X, AGENT_X]:
        fig.add_shape(
            type="line",
            xref="x4",
            yref="paper",
            x0=x_pos,
            x1=x_pos,
            y0=0,
            y1=1,
            line=dict(color="rgba(100,100,100,0.16)", width=1, dash="dot"),
        )

    for i, tag in enumerate(tag_intervals, start=1):
        label = tag.get("label", f"Tag {i}")
        hover_text = f"Tagger<br>{label}"
        _add_vertical_interval_line(
            fig=fig,
            x_pos=TAG_X,
            start_time=tag["start"],
            end_time=tag["end"],
            color="rgba(128, 0, 128, 0.85)",
            width=4,
            row=row,
            col=col,
            hover_text=hover_text,
        )

    for overlap in overlap_intervals:
        hover_text = (
            "Overlap<br>"
            f"Tag: {overlap.get('tag_label', '')}<br>"
            f"Agent: {overlap.get('agent_label', '')}"
        )
        _add_vertical_interval_line(
            fig=fig,
            x_pos=OVERLAP_X,
            start_time=overlap["start"],
            end_time=overlap["end"],
            color="rgba(60, 160, 90, 0.90)",
            width=5,
            row=row,
            col=col,
            hover_text=hover_text,
        )

    for i, agent in enumerate(agent_intervals, start=1):
        label = agent.get("label", f"Hit {i}")
        severity = agent.get("severity", "Medium")
        hover_text = f"Agent hit<br>{label}<br>Severity: {severity}"
        _add_vertical_interval_line(
            fig=fig,
            x_pos=AGENT_X,
            start_time=agent["start"],
            end_time=agent["end"],
            color="rgba(220, 50, 47, 0.92)",
            width=_agent_line_width(severity),
            row=row,
            col=col,
            hover_text=hover_text,
        )

    fig.add_annotation(
        xref="x4", yref="paper", x=TAG_X, y=1.03,
        text="<b>Tagger</b>",
        showarrow=False, font=dict(size=10, color="#6A0DAD")
    )
    fig.add_annotation(
        xref="x4", yref="paper", x=OVERLAP_X, y=1.03,
        text="<b>Overlap</b>",
        showarrow=False, font=dict(size=10, color="#2E8B57")
    )
    fig.add_annotation(
        xref="x4", yref="paper", x=AGENT_X, y=1.03,
        text="<b>Agent</b>",
        showarrow=False, font=dict(size=10, color="#C0392B")
    )

    summary = agent_cfg.get("summary", {})
    summary_text = (
        f"Tags: {summary.get('tag_count', 0)}"
        f" &nbsp;|&nbsp; Hits: {summary.get('agent_count', 0)}"
        f" &nbsp;|&nbsp; Overlap: {summary.get('overlap_count', 0)} / {summary.get('tag_count', 0)}"
    )
    fig.add_annotation(
        xref="x4",
        yref="paper",
        x=0.5,
        y=-0.09,
        text=summary_text,
        showarrow=False,
        font=dict(size=10, color="#444"),
    )

    fig.update_xaxes(
        row=row,
        col=col,
        range=list(AGENT_TRACK_XRANGE),
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        side="top",
        title_text="",
    )


def _add_track_scale_guides(fig: go.Figure, track_idx: int):
    axis_name = "x domain" if track_idx == 0 else f"x{track_idx + 1} domain"

    for xpos in [0.0, 0.5, 1.0]:
        fig.add_shape(
            type="line",
            xref=axis_name,
            yref="paper",
            x0=xpos,
            x1=xpos,
            y0=0,
            y1=1,
            line=dict(color="rgba(120,120,120,0.10)", width=1, dash="dot"),
        )


def _add_scale_row(fig: go.Figure, track_idx: int, param_idx: int, label: str, color: str, x_min: float, x_max: float):
    axis_name = "x domain" if track_idx == 0 else f"x{track_idx + 1} domain"
    y_pos = -0.09 - (param_idx * 0.052)

    fig.add_annotation(
        xref=axis_name,
        yref="paper",
        x=0.01,
        y=y_pos,
        text=f"<span style='color:{color}'><b>{label}</b></span>",
        showarrow=False,
        xanchor="left",
        font=dict(size=10),
    )
    fig.add_annotation(
        xref=axis_name,
        yref="paper",
        x=0.16,
        y=y_pos,
        text=f"<span style='color:{color}'>{format_number(x_min)}</span>",
        showarrow=False,
        xanchor="left",
        font=dict(size=10),
    )
    fig.add_annotation(
        xref=axis_name,
        yref="paper",
        x=0.84,
        y=y_pos,
        text=f"<span style='color:{color}'>{format_number(x_max)}</span>",
        showarrow=False,
        xanchor="right",
        font=dict(size=10),
    )


def create_multi_track_chart(
    df: pd.DataFrame,
    track_params: list[list[str]],
    track_param_labels: list[list[str]],
    track_colors: list[list[str]],
    zoom_percent: float,
    section_ranges: list[dict] | None = None,
    agent_cfg: dict | None = None,
    chart_height: int = 950,
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

    for track_idx in range(3):
        params = track_params[track_idx]
        labels = track_param_labels[track_idx]
        colors = track_colors[track_idx]

        _add_track_scale_guides(fig, track_idx)

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

            _add_scale_row(fig, track_idx, param_idx, label, color, x_min, x_max)

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

    if agent_cfg:
        add_agent_track(fig, agent_cfg, row=1, col=4)

    if section_ranges and t_min_view is not None and t_max_view is not None:
        add_section_boundaries(fig, section_ranges, t_min_view, t_max_view)

    if agent_cfg and agent_cfg.get("show_reference_line") and agent_cfg.get("reference_time") is not None:
        add_reference_line(fig, agent_cfg["reference_time"])

    y_range = None
    if t_min_view is not None and t_max_view is not None:
        y_range = [t_max_view, t_min_view]

    tickvals, ticktext = _build_dual_time_ticks(t_min_view, t_max_view, n_ticks=12)

    fig.update_yaxes(
        range=y_range,
        autorange=False if y_range else "reversed",
        showgrid=True,
        gridcolor="rgba(140,140,140,0.20)",
        gridwidth=0.6,
        tickmode="array" if tickvals is not None else "auto",
        tickvals=tickvals,
        ticktext=ticktext,
        tickfont=dict(size=10, family="Courier New"),
    )

    fig.add_annotation(
        xref="paper",
        yref="paper",
        x=0.0,
        y=1.03,
        text="<b>Date</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Time</b>",
        showarrow=False,
        xanchor="left",
        font=dict(size=10, color="#333"),
    )

    fig.update_layout(
        height=chart_height,
        margin=dict(l=120, r=20, t=75, b=170),
        hovermode="closest",
        plot_bgcolor="white",
        paper_bgcolor="white",
        uirevision="keep_zoom_state",
    )

    return fig