import requests
import streamlit as st

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Solar Inspection Dashboard",
    page_icon="☀️",
    layout="wide",
)

st.title("☀️ Solar Panel Inspection Dashboard")
st.caption("Drone-based YOLOv8 inspection and mission analytics")

# --------------------------------------------------
# API helpers
# --------------------------------------------------


def api_get(endpoint):
    try:
        response = requests.get(
            f"{API_URL}{endpoint}",
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except Exception as exc:  # noqa: BLE001
        st.error(f"API connection failed: {exc}")
        return None


# --------------------------------------------------
# Backend health
# --------------------------------------------------

health = api_get("/health")

if health:
    st.success("API online")
else:
    st.error("API unavailable")


# --------------------------------------------------
# Missions
# --------------------------------------------------

data = api_get("/missions")

if not data:
    st.warning("No mission data available.")
    st.stop()

missions = data.get("missions", [])

if not missions:
    st.warning("No missions found.")
    st.stop()

selected_mission = st.selectbox(
    "Select Mission",
    missions,
    index=len(missions) - 1,
)

mission = api_get(f"/missions/{selected_mission}")

report = api_get(f"/missions/{selected_mission}/report")

# --------------------------------------------------
# Mission summary
# --------------------------------------------------

if report:

    status = report.get("status", "UNKNOWN")

    if status == "CRITICAL":
        st.error(f"MISSION STATUS: {status}")
    elif status == "WARNING":
        st.warning(f"MISSION STATUS: {status}")
    else:
        st.success(f"MISSION STATUS: {status}")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Images",
        report.get("images_inspected", 0),
    )

    col2.metric(
        "Detections",
        report.get("total_detections", 0),
    )

    col3.metric(
        "Critical",
        report.get("critical_detections", 0),
    )

    col4.metric(
        "Confidence",
        f"{report.get('average_confidence', 0) * 100:.2f}%",
    )

    st.divider()

    # --------------------------------------------------
    # Detection classes
    # --------------------------------------------------

    st.subheader("Detection Analytics")

    counts = report.get(
        "detections_by_class",
        report.get("class_counts", {}),
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Panels",
        counts.get("panel", 0),
    )

    c2.metric(
        "Cracked",
        counts.get("cracked", 0),
    )

    c3.metric(
        "Dusty",
        counts.get("dusty", 0),
    )

    if counts:
        st.bar_chart(counts)

    # --------------------------------------------------
    # Mission health
    # --------------------------------------------------

    health_data = report.get("health", {})

    st.subheader("Mission Health")

    h1, h2, h3 = st.columns(3)

    h1.metric(
        "Defects",
        health_data.get("defect_detections", 0),
    )

    h2.metric(
        "Defect Ratio",
        f"{health_data.get('defect_ratio', 0) * 100:.2f}%",
    )

    h3.metric(
        "Health Status",
        health_data.get("status", "UNKNOWN"),
    )

    recommendation = health_data.get(
        "recommendation",
        report.get("recommendation", ""),
    )

    if recommendation:
        st.info(f"**Recommendation:** {recommendation}")

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    if mission:
        st.subheader("Mission Metadata")

        metadata = mission.get(
            "metadata",
            {},
        )

        st.json(metadata)

else:
    st.warning("Unable to load mission report.")
