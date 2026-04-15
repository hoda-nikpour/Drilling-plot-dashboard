import streamlit as st

from config import MAX_PARAMS_PER_TRACK, PARAMETER_DISPLAY_NAMES


def render_well_section_selector(sections_by_well: dict):
    with st.sidebar:
        st.subheader("Well")
        selected_well = st.selectbox(
            "Select Well",
            options=sorted(sections_by_well.keys()),
            index=0,
            key="selected_well",
        )

        available_sections = sorted(sections_by_well.get(selected_well, []), key=float)

        st.subheader("Section")
        selected_sections = st.multiselect(
            "Select Section(s)",
            options=available_sections,
            default=[],
            format_func=lambda s: f'{s}"',
            key=f"selected_sections_{selected_well}",
        )

    return selected_well, selected_sections


def render_track_parameter_selector(available_param_labels: list[str], context_key: str):
    with st.sidebar:
        st.subheader("Track Parameters (Tracks 1–3)")

        track_params = []
        for i in range(3):
            selected = st.multiselect(
                f"Track {i + 1} parameters (max {MAX_PARAMS_PER_TRACK})",
                options=available_param_labels,
                default=[],
                max_selections=MAX_PARAMS_PER_TRACK,
                key=f"track_params_{i + 1}_{context_key}",
                format_func=lambda p: PARAMETER_DISPLAY_NAMES.get(p, p),
            )
            track_params.append(selected)

    return track_params


def render_time_filter(df, context_key: str):
    with st.sidebar:
        st.subheader("Time Filter")

        t_min_all = df.index.min().to_pydatetime()
        t_max_all = df.index.max().to_pydatetime()

        time_range = st.slider(
            "Select Time Range",
            min_value=t_min_all,
            max_value=t_max_all,
            value=(t_min_all, t_max_all),
            format="YYYY-MM-DD HH:mm",
            key=f"time_range_{context_key}",
        )

        total_sec = (t_max_all - t_min_all).total_seconds()
        sel_sec = (time_range[1] - time_range[0]).total_seconds()
        zoom_percent = 100.0 - (sel_sec / total_sec * 100.0) if total_sec > 0 else 0.0

        st.metric("Records", f"{len(df):,}")
        st.metric("Zoom", f"{zoom_percent:.0f}%")

    return time_range, zoom_percent


def render_agent_controls(df, context_key: str):
    with st.sidebar:
        st.subheader("Track 4 — Data Agent")

        t_min = df.index.min().to_pydatetime()
        t_max = df.index.max().to_pydatetime()

        enable_tag = st.checkbox(
            "Show tagged area",
            value=True,
            key=f"enable_tag_{context_key}",
        )

        tag_range = st.slider(
            "Tagged interval",
            min_value=t_min,
            max_value=t_max,
            value=(t_min, t_max),
            format="YYYY-MM-DD HH:mm",
            key=f"tag_range_{context_key}",
        )

        enable_agent = st.checkbox(
            "Show resulting data agent",
            value=True,
            key=f"enable_agent_{context_key}",
        )

        agent_range = st.slider(
            "Agent result interval",
            min_value=t_min,
            max_value=t_max,
            value=(t_min, t_max),
            format="YYYY-MM-DD HH:mm",
            key=f"agent_range_{context_key}",
        )

        severity = st.selectbox(
            "Agent severity",
            options=["Low", "Medium", "High"],
            index=1,
            key=f"agent_severity_{context_key}",
        )

        return {
            "enable_tag": enable_tag,
            "tag_start": tag_range[0],
            "tag_end": tag_range[1],
            "enable_agent": enable_agent,
            "agent_start": agent_range[0],
            "agent_end": agent_range[1],
            "severity": severity,
        }