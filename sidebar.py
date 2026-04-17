
# import csv
# import io
# import json

# import pandas as pd
# import streamlit as st

# from config import MAX_PARAMS_PER_TRACK, PARAMETER_DISPLAY_NAMES


# def _interval_overlap(a_start, a_end, b_start, b_end):
#     start = max(pd.Timestamp(a_start), pd.Timestamp(b_start))
#     end = min(pd.Timestamp(a_end), pd.Timestamp(b_end))
#     if start < end:
#         return start, end
#     return None


# def _build_summary(tag_intervals: list[dict], agent_intervals: list[dict]) -> dict:
#     overlap_count = 0
#     for tag in tag_intervals:
#         tag_has_overlap = False
#         for agent in agent_intervals:
#             if _interval_overlap(tag["start"], tag["end"], agent["start"], agent["end"]) is not None:
#                 tag_has_overlap = True
#                 break
#         if tag_has_overlap:
#             overlap_count += 1

#     return {
#         "tag_count": len(tag_intervals),
#         "agent_count": len(agent_intervals),
#         "overlap_count": overlap_count,
#     }


# def _build_export_payload(tag_intervals: list[dict], agent_intervals: list[dict], summary: dict) -> tuple[str, str]:
#     payload = {
#         "tag_intervals": [
#             {
#                 "label": x["label"],
#                 "start": str(x["start"]),
#                 "end": str(x["end"]),
#             }
#             for x in tag_intervals
#         ],
#         "agent_intervals": [
#             {
#                 "label": x["label"],
#                 "start": str(x["start"]),
#                 "end": str(x["end"]),
#                 "severity": x["severity"],
#             }
#             for x in agent_intervals
#         ],
#         "summary": summary,
#     }
#     json_text = json.dumps(payload, indent=2)

#     output = io.StringIO()
#     writer = csv.writer(output)
#     writer.writerow(["type", "label", "start", "end", "severity"])
#     for item in tag_intervals:
#         writer.writerow(["tag", item["label"], item["start"], item["end"], ""])
#     for item in agent_intervals:
#         writer.writerow(["agent", item["label"], item["start"], item["end"], item["severity"]])

#     return json_text, output.getvalue()


# def render_well_section_selector(sections_by_well: dict):
#     with st.sidebar:
#         st.subheader("Well")
#         selected_well = st.selectbox(
#             "Select Well",
#             options=sorted(sections_by_well.keys()),
#             index=0,
#             key="selected_well",
#         )

#         available_sections = sorted(sections_by_well.get(selected_well, []), key=float)

#         st.subheader("Section")
#         selected_sections = st.multiselect(
#             "Select Section(s)",
#             options=available_sections,
#             default=[],
#             format_func=lambda s: f'{s}"',
#             key=f"selected_sections_{selected_well}",
#         )

#     return selected_well, selected_sections


# def render_track_parameter_selector(available_param_labels: list[str], context_key: str):
#     with st.sidebar:
#         st.subheader("Track Parameters (Tracks 1–3)")

#         track_params = []
#         for i in range(3):
#             selected = st.multiselect(
#                 f"Track {i + 1} parameters (max {MAX_PARAMS_PER_TRACK})",
#                 options=available_param_labels,
#                 default=[],
#                 max_selections=MAX_PARAMS_PER_TRACK,
#                 key=f"track_params_{i + 1}_{context_key}",
#                 format_func=lambda p: PARAMETER_DISPLAY_NAMES.get(p, p),
#             )
#             track_params.append(selected)

#     return track_params


# def render_time_filter(df, context_key: str):
#     with st.sidebar:
#         st.subheader("Time Filter")

#         t_min_all = df.index.min().to_pydatetime()
#         t_max_all = df.index.max().to_pydatetime()

#         time_range = st.slider(
#             "Select Time Range",
#             min_value=t_min_all,
#             max_value=t_max_all,
#             value=(t_min_all, t_max_all),
#             format="YYYY-MM-DD HH:mm",
#             key=f"time_range_{context_key}",
#         )

#         total_sec = (t_max_all - t_min_all).total_seconds()
#         sel_sec = (time_range[1] - time_range[0]).total_seconds()
#         zoom_percent = 100.0 - (sel_sec / total_sec * 100.0) if total_sec > 0 else 0.0

#         st.metric("Records", f"{len(df):,}")
#         st.metric("Zoom", f"{zoom_percent:.0f}%")

#     return time_range, zoom_percent


# def render_agent_controls(df, context_key: str):
#     with st.sidebar:
#         st.subheader("Track 4 — Review Track")

#         t_min = df.index.min().to_pydatetime()
#         t_max = df.index.max().to_pydatetime()

#         height_mode = st.selectbox(
#             "Chart height",
#             options=["Normal", "Stretched"],
#             index=0,
#             key=f"height_mode_{context_key}",
#         )
#         chart_height = 860 if height_mode == "Normal" else 1200

#         show_reference_line = st.checkbox(
#             "Show cross-track reference line",
#             value=False,
#             key=f"show_reference_line_{context_key}",
#         )

#         reference_time = None
#         if show_reference_line:
#             reference_time = st.slider(
#                 "Reference time",
#                 min_value=t_min,
#                 max_value=t_max,
#                 value=t_min,
#                 format="YYYY-MM-DD HH:mm",
#                 key=f"reference_time_{context_key}",
#             )

#         tag_intervals = []
#         agent_intervals = []

#         st.markdown("**Tagger lane**")
#         for i in range(1, 4):
#             enabled = st.checkbox(
#                 f"Enable Tag {i}",
#                 value=(i == 1),
#                 key=f"enable_tag_{i}_{context_key}",
#             )
#             if enabled:
#                 label = st.text_input(
#                     f"Tag {i} label",
#                     value=f"Observation {i}",
#                     key=f"tag_label_{i}_{context_key}",
#                 )
#                 interval = st.slider(
#                     f"Tag {i} interval",
#                     min_value=t_min,
#                     max_value=t_max,
#                     value=(t_min, t_max),
#                     format="YYYY-MM-DD HH:mm",
#                     key=f"tag_interval_{i}_{context_key}",
#                 )
#                 tag_intervals.append(
#                     {
#                         "label": label.strip() or f"Observation {i}",
#                         "start": interval[0],
#                         "end": interval[1],
#                     }
#                 )

#         st.markdown("**Agent lane**")
#         for i in range(1, 4):
#             enabled = st.checkbox(
#                 f"Enable Agent Hit {i}",
#                 value=(i == 1),
#                 key=f"enable_agent_{i}_{context_key}",
#             )
#             if enabled:
#                 label = st.text_input(
#                     f"Agent Hit {i} label",
#                     value=f"Hit {i}",
#                     key=f"agent_label_{i}_{context_key}",
#                 )
#                 interval = st.slider(
#                     f"Agent Hit {i} interval",
#                     min_value=t_min,
#                     max_value=t_max,
#                     value=(t_min, t_max),
#                     format="YYYY-MM-DD HH:mm",
#                     key=f"agent_interval_{i}_{context_key}",
#                 )
#                 severity = st.selectbox(
#                     f"Agent Hit {i} severity",
#                     options=["Low", "Medium", "High"],
#                     index=1,
#                     key=f"agent_severity_{i}_{context_key}",
#                 )
#                 agent_intervals.append(
#                     {
#                         "label": label.strip() or f"Hit {i}",
#                         "start": interval[0],
#                         "end": interval[1],
#                         "severity": severity,
#                     }
#                 )

#         summary = _build_summary(tag_intervals, agent_intervals)
#         st.caption(
#             f"Summary — Tags: {summary['tag_count']} | "
#             f"Hits: {summary['agent_count']} | "
#             f"Overlap: {summary['overlap_count']} / {summary['tag_count']}"
#         )

#         json_text, csv_text = _build_export_payload(tag_intervals, agent_intervals, summary)

#         st.download_button(
#             "Export tags/hits as JSON",
#             data=json_text,
#             file_name=f"tag_review_{context_key}.json",
#             mime="application/json",
#             key=f"download_json_{context_key}",
#         )

#         st.download_button(
#             "Export tags/hits as CSV",
#             data=csv_text,
#             file_name=f"tag_review_{context_key}.csv",
#             mime="text/csv",
#             key=f"download_csv_{context_key}",
#         )

#         return {
#             "tag_intervals": tag_intervals,
#             "agent_intervals": agent_intervals,
#             "summary": summary,
#             "show_reference_line": show_reference_line,
#             "reference_time": reference_time,
#             "chart_height": chart_height,
#         }

import csv
import io
import json

import pandas as pd
import streamlit as st

from config import MAX_PARAMS_PER_TRACK, PARAMETER_DISPLAY_NAMES


def _interval_overlap(a_start, a_end, b_start, b_end):
    start = max(pd.Timestamp(a_start), pd.Timestamp(b_start))
    end = min(pd.Timestamp(a_end), pd.Timestamp(b_end))
    if start < end:
        return start, end
    return None


def _build_tag_status_rows(tag_intervals: list[dict], agent_intervals: list[dict]) -> list[dict]:
    rows = []
    for tag in tag_intervals:
        matched = False
        overlap_start = None
        overlap_end = None
        for agent in agent_intervals:
            ov = _interval_overlap(tag["start"], tag["end"], agent["start"], agent["end"])
            if ov is not None:
                matched = True
                overlap_start, overlap_end = ov
                break

        rows.append(
            {
                "label": tag["label"],
                "start": tag["start"],
                "end": tag["end"],
                "status": "Matched" if matched else "Unmatched",
                "overlap_start": overlap_start,
                "overlap_end": overlap_end,
            }
        )
    return rows


def _build_summary(tag_intervals: list[dict], agent_intervals: list[dict]) -> dict:
    tag_status_rows = _build_tag_status_rows(tag_intervals, agent_intervals)
    overlap_count = sum(1 for row in tag_status_rows if row["status"] == "Matched")
    return {
        "tag_count": len(tag_intervals),
        "agent_count": len(agent_intervals),
        "overlap_count": overlap_count,
        "tag_status_rows": tag_status_rows,
    }


def _build_export_payload(tag_intervals: list[dict], agent_intervals: list[dict], summary: dict) -> tuple[str, str]:
    payload = {
        "tag_intervals": [
            {
                "label": x["label"],
                "start": str(x["start"]),
                "end": str(x["end"]),
            }
            for x in tag_intervals
        ],
        "agent_intervals": [
            {
                "label": x["label"],
                "start": str(x["start"]),
                "end": str(x["end"]),
                "severity": x["severity"],
            }
            for x in agent_intervals
        ],
        "summary": {
            "tag_count": summary["tag_count"],
            "agent_count": summary["agent_count"],
            "overlap_count": summary["overlap_count"],
        },
    }
    json_text = json.dumps(payload, indent=2)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["type", "label", "start", "end", "severity"])
    for item in tag_intervals:
        writer.writerow(["tag", item["label"], item["start"], item["end"], ""])
    for item in agent_intervals:
        writer.writerow(["agent", item["label"], item["start"], item["end"], item["severity"]])

    return json_text, output.getvalue()


def _apply_loaded_review_to_state(uploaded_data: dict, context_key: str):
    for i in range(1, 4):
        st.session_state[f"enable_tag_{i}_{context_key}"] = False
        st.session_state[f"enable_agent_{i}_{context_key}"] = False

    for i, tag in enumerate(uploaded_data.get("tag_intervals", [])[:3], start=1):
        st.session_state[f"enable_tag_{i}_{context_key}"] = True
        st.session_state[f"tag_label_{i}_{context_key}"] = tag.get("label", f"Observation {i}")
        st.session_state[f"tag_interval_{i}_{context_key}"] = (
            pd.to_datetime(tag["start"]).to_pydatetime(),
            pd.to_datetime(tag["end"]).to_pydatetime(),
        )

    for i, agent in enumerate(uploaded_data.get("agent_intervals", [])[:3], start=1):
        st.session_state[f"enable_agent_{i}_{context_key}"] = True
        st.session_state[f"agent_label_{i}_{context_key}"] = agent.get("label", f"Hit {i}")
        st.session_state[f"agent_interval_{i}_{context_key}"] = (
            pd.to_datetime(agent["start"]).to_pydatetime(),
            pd.to_datetime(agent["end"]).to_pydatetime(),
        )
        st.session_state[f"agent_severity_{i}_{context_key}"] = agent.get("severity", "Medium")


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
        st.subheader("Track 4 — Simple Review Track")

        t_min = df.index.min().to_pydatetime()
        t_max = df.index.max().to_pydatetime()

        review_mode = st.selectbox(
            "Review mode",
            options=["Standard review", "Stretched inspection"],
            index=1,
            key=f"review_mode_{context_key}",
        )
        chart_height = 950 if review_mode == "Standard review" else 1400

        uploaded_review = st.file_uploader(
            "Load saved review JSON",
            type=["json"],
            key=f"review_upload_{context_key}",
        )
        if uploaded_review is not None:
            try:
                uploaded_data = json.load(uploaded_review)
                _apply_loaded_review_to_state(uploaded_data, context_key)
                st.success("Saved review loaded into the controls.")
            except Exception:
                st.error("Could not read the uploaded review JSON.")

        show_reference_line = st.checkbox(
            "Show cross-track reference line",
            value=False,
            key=f"show_reference_line_{context_key}",
        )

        reference_time = None
        if show_reference_line:
            reference_time = st.slider(
                "Reference time",
                min_value=t_min,
                max_value=t_max,
                value=t_min,
                format="YYYY-MM-DD HH:mm",
                key=f"reference_time_{context_key}",
            )

        tag_intervals = []
        agent_intervals = []

        st.markdown("**Tagger lane**")
        for i in range(1, 4):
            enabled = st.checkbox(
                f"Enable Tag {i}",
                value=(i == 1),
                key=f"enable_tag_{i}_{context_key}",
            )
            if enabled:
                label = st.text_input(
                    f"Tag {i} label",
                    value=f"Observation {i}",
                    key=f"tag_label_{i}_{context_key}",
                )
                interval = st.slider(
                    f"Tag {i} interval",
                    min_value=t_min,
                    max_value=t_max,
                    value=(t_min, t_max),
                    format="YYYY-MM-DD HH:mm",
                    key=f"tag_interval_{i}_{context_key}",
                )
                tag_intervals.append(
                    {
                        "label": label.strip() or f"Observation {i}",
                        "start": interval[0],
                        "end": interval[1],
                    }
                )

        st.markdown("**Agent lane**")
        for i in range(1, 4):
            enabled = st.checkbox(
                f"Enable Agent Hit {i}",
                value=(i == 1),
                key=f"enable_agent_{i}_{context_key}",
            )
            if enabled:
                label = st.text_input(
                    f"Agent Hit {i} label",
                    value=f"Hit {i}",
                    key=f"agent_label_{i}_{context_key}",
                )
                interval = st.slider(
                    f"Agent Hit {i} interval",
                    min_value=t_min,
                    max_value=t_max,
                    value=(t_min, t_max),
                    format="YYYY-MM-DD HH:mm",
                    key=f"agent_interval_{i}_{context_key}",
                )
                severity = st.selectbox(
                    f"Agent Hit {i} severity",
                    options=["Low", "Medium", "High"],
                    index=1,
                    key=f"agent_severity_{i}_{context_key}",
                )
                agent_intervals.append(
                    {
                        "label": label.strip() or f"Hit {i}",
                        "start": interval[0],
                        "end": interval[1],
                        "severity": severity,
                    }
                )

        summary = _build_summary(tag_intervals, agent_intervals)
        st.caption(
            f"Summary — Tags: {summary['tag_count']} | "
            f"Hits: {summary['agent_count']} | "
            f"Overlap: {summary['overlap_count']} / {summary['tag_count']}"
        )

        status_rows = summary["tag_status_rows"]
        if status_rows:
            st.markdown("**Manual review status**")
            for row in status_rows:
                st.caption(f"{row['label']}: {row['status']}")

        json_text, csv_text = _build_export_payload(tag_intervals, agent_intervals, summary)

        st.download_button(
            "Export tags/hits as JSON",
            data=json_text,
            file_name=f"tag_review_{context_key}.json",
            mime="application/json",
            key=f"download_json_{context_key}",
        )

        st.download_button(
            "Export tags/hits as CSV",
            data=csv_text,
            file_name=f"tag_review_{context_key}.csv",
            mime="text/csv",
            key=f"download_csv_{context_key}",
        )

        return {
            "tag_intervals": tag_intervals,
            "agent_intervals": agent_intervals,
            "summary": summary,
            "show_reference_line": show_reference_line,
            "reference_time": reference_time,
            "chart_height": chart_height,
            "review_mode": review_mode,
        }