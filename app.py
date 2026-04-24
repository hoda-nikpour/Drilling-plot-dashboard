import pandas as pd
import streamlit as st

from chart_builder import create_multi_track_chart
from config import PARAMETER_ALIASES, PARAMETER_CATALOG, TRACK_COLOR_PALETTE
from data_loader import (
    get_available_numeric_columns,
    load_catalog,
    load_sections_for_columns,
)
from helpers import compute_section_ranges
from sidebar import (
    render_agent_controls,
    render_parameter_range_controls,
    render_plot_style_controls,
    render_time_filter,
    render_track_parameter_selector,
    render_well_section_selector,
)

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 4.0rem;
        padding-bottom: 0;
    }

    .well-header {
        text-align: center;
        color: #1E3A5F;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .well-subheader {
        text-align: center;
        color: #555;
        font-size: 0.85rem;
        margin-bottom: 0rem;
    }

    div[data-testid="stPlotlyChart"] {
        position: relative;
        padding-top: 18px;
    }

    div[data-testid="stPlotlyChart"] .modebar-container {
        position: absolute !important;
        top: -8px !important;
        left: 0 !important;
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        pointer-events: none !important;
        z-index: 1000 !important;
    }

    div[data-testid="stPlotlyChart"] .modebar {
        position: relative !important;
        left: auto !important;
        right: auto !important;
        top: 0 !important;
        opacity: 1 !important;
        visibility: visible !important;
        display: flex !important;
        background: #f3f3f3 !important;
        border: 1px solid #d0d0d0 !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        padding: 3px 6px !important;
        pointer-events: auto !important;
    }

    div[data-testid="stPlotlyChart"] .modebar-group {
        background: transparent !important;
        border: none !important;
        padding-left: 2px !important;
        padding-right: 2px !important;
    }

    div[data-testid="stPlotlyChart"] a.modebar-btn {
        opacity: 1 !important;
    }

    div[data-testid="stPlotlyChart"] svg.icon {
        width: 18px !important;
        height: 18px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def build_sections_by_well(catalog: dict) -> dict[str, list[str]]:
    sections_by_well = {}
    for entry in catalog["sections"]:
        well = entry["well"]
        section = str(entry["section_in"])
        sections_by_well.setdefault(well, []).append(section)
    return sections_by_well


def flatten_selected_params(track_params: list[list[str]]) -> list[str]:
    seen = []
    for group in track_params:
        for item in group:
            if item not in seen:
                seen.append(item)
    return seen


def build_label_to_column_map(discovered_params: list[str]) -> dict[str, str]:
    discovered_set = set(discovered_params)
    label_to_column = {}

    for label, aliases in PARAMETER_ALIASES.items():
        for alias in aliases:
            if alias in discovered_set:
                label_to_column[label] = alias
                break

    return label_to_column


def make_context_key(selected_well: str, selected_sections: tuple[str, ...]) -> str:
    return f"{selected_well}__{'_'.join(selected_sections)}"


def build_parameter_catalog_df(label_to_column: dict[str, str]) -> pd.DataFrame:
    rows = []
    for label, raw_col in label_to_column.items():
        meta = PARAMETER_CATALOG.get(label, {})
        rows.append(
            {
                "Parameter": label,
                "Raw mnemonic": raw_col,
                "Meaning": meta.get("meaning", ""),
                "Unit": meta.get("unit", ""),
                "Logical min": meta.get("logical_min", ""),
                "Logical max": meta.get("logical_max", ""),
            }
        )
    return pd.DataFrame(rows).sort_values("Parameter").reset_index(drop=True)


def build_manual_review_df(summary: dict) -> pd.DataFrame:
    rows = summary.get("tag_status_rows", [])
    if not rows:
        return pd.DataFrame(columns=["Tag", "Start", "End", "Status", "Overlap Start", "Overlap End"])

    return pd.DataFrame(
        [
            {
                "Tag": row["label"],
                "Start": row["start"],
                "End": row["end"],
                "Status": row["status"],
                "Overlap Start": row["overlap_start"],
                "Overlap End": row["overlap_end"],
            }
            for row in rows
        ]
    )


def main():
    catalog = load_catalog()
    if not catalog["sections"]:
        st.error("data/catalog.json not found or empty.")
        st.stop()

    sections_by_well = build_sections_by_well(catalog)
    selected_well, selected_sections = render_well_section_selector(sections_by_well)

    if not selected_sections:
        st.warning("Please select at least one section from the sidebar.")
        st.stop()

    selected_sections = tuple(sorted(selected_sections, key=float))
    context_key = make_context_key(selected_well, selected_sections)

    discovered_params = get_available_numeric_columns(selected_well, selected_sections)
    label_to_column = build_label_to_column_map(discovered_params)
    available_param_labels = list(label_to_column.keys())

    if not available_param_labels:
        st.error(
            "None of the requested drilling parameters were found for the selected well/sections. "
            f"Found numeric columns: {', '.join(discovered_params[:30])}"
        )
        st.stop()

    with st.expander("Parameter catalog for review", expanded=False):
        st.dataframe(build_parameter_catalog_df(label_to_column), use_container_width=True)

    track_param_labels = render_track_parameter_selector(available_param_labels, context_key)
    selected_labels = flatten_selected_params(track_param_labels)

    if not selected_labels:
        st.info("Select parameters from the sidebar to display plots.")
        st.stop()

    parameter_ranges = render_parameter_range_controls(selected_labels, context_key)
    marker_setting = render_plot_style_controls(context_key)

    requested_columns = [label_to_column[label] for label in selected_labels]

    df = load_sections_for_columns(
        well=selected_well,
        sections=selected_sections,
        requested_columns=tuple(requested_columns),
    )

    if df.empty:
        st.error("No data loaded. Check the parquet files in the data folder.")
        st.stop()

    time_range, zoom_percent = render_time_filter(df, context_key)

    df = df.loc[pd.Timestamp(time_range[0]): pd.Timestamp(time_range[1])]
    if df.empty:
        st.warning("No data available in the selected time range.")
        st.stop()

    agent_cfg = render_agent_controls(df, context_key)

    section_ranges = compute_section_ranges(df, list(selected_sections))

    sections_label = "  ·  ".join(f'{s}"' for s in selected_sections)
    st.markdown(
        f'<div class="well-header">Well {selected_well}</div>'
        f'<div class="well-subheader">Mud Logging Dashboard &nbsp;|&nbsp; '
        f'Sections: {sections_label} &nbsp;|&nbsp; Review mode: {agent_cfg.get("review_mode", "Standard review")}</div>',
        unsafe_allow_html=True,
    )

    summary = agent_cfg.get("summary", {})
    accepted_text = "Accepted" if summary.get("accepted", False) else "Not accepted yet"

    st.caption(
        f"Review summary — Tags: {summary.get('tag_count', 0)} | "
        f"Hits: {summary.get('agent_count', 0)} | "
        f"Overlap: {summary.get('overlap_count', 0)} / {summary.get('tag_count', 0)} | "
        f"Score: {summary.get('score_percent', 0.0):.1f}% | "
        f"Status: {accepted_text}"
    )

    review_df = build_manual_review_df(summary)
    if not review_df.empty:
        with st.expander("Manual hit review", expanded=False):
            st.dataframe(review_df, use_container_width=True)

    track_colors = [TRACK_COLOR_PALETTE[:len(params)] for params in track_param_labels]

    track_params_real = [
        [label_to_column[label] for label in track if label in label_to_column]
        for track in track_param_labels
    ]

    track_params_real = track_params_real + [[]]
    track_param_labels = track_param_labels + [[]]
    track_colors = track_colors + [[]]

    fig = create_multi_track_chart(
        df=df,
        track_params=track_params_real,
        track_param_labels=track_param_labels,
        track_colors=track_colors,
        zoom_percent=zoom_percent,
        section_ranges=section_ranges,
        agent_cfg=agent_cfg,
        chart_height=agent_cfg.get("chart_height", 950),
        parameter_ranges=parameter_ranges,
        marker_setting=marker_setting,
    )

    chart_key = f"multi_track_chart_{context_key}"

    st.caption(
        "Chart controls: use the toolbar above the chart or double-click inside the chart to reset zoom. "
        "Use 'Reset time filter' in the sidebar to restore the full selected time window."
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key=chart_key,
        config={
            "displaylogo": False,
            "displayModeBar": True,
            "scrollZoom": False,
            "doubleClick": "reset+autosize",
            "modeBarButtonsToRemove": [
                "lasso2d",
                "select2d",
                "toggleSpikelines",
            ],
        },
    )


if __name__ == "__main__":
    main()