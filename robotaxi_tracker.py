"""
Vibe Robotaxi Tracker - Las Vegas
Pure Python Streamlit version of the live robotaxi dashboard.
"""

import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime
import folium
from streamlit_folium import st_folium
from streamlit_autorefresh import st_autorefresh

# Page config
st.set_page_config(
    page_title="Vibe Robotaxi Tracker | Las Vegas",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme vibe
st.markdown("""
<style>
    .stApp {
        background-color: #09090b;
        color: #e4e4e7;
    }
    .stMetric {
        background-color: #18181b;
        border: 1px solid #27272a;
        border-radius: 16px;
        padding: 12px;
    }
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
    }
    .provider-zoox { color: #00f0ff; }
    .provider-waymo { color: #a855f7; }
    .provider-cybercab { color: #e82127; }
</style>
""", unsafe_allow_html=True)

# Initial vehicle data
INITIAL_VEHICLES = [
    {"id": "ZOX-LV-042", "provider": "Zoox", "status": "Active", "lat": 36.1147, "lng": -115.1728, "location": "Las Vegas Strip (Bellagio)", "last_updated": "Just now", "speed": 28, "trips": 312},
    {"id": "ZOX-LV-019", "provider": "Zoox", "status": "Charging", "lat": 36.0801, "lng": -115.1534, "location": "Harry Reid Airport Hub", "last_updated": "9 min ago", "speed": 0, "trips": 421},
    {"id": "ZOX-LV-023", "provider": "Zoox", "status": "Idle", "lat": 36.1953, "lng": -115.1214, "location": "North Las Vegas", "last_updated": "14 min ago", "speed": 0, "trips": 267},
    {"id": "ZOX-LV-066", "provider": "Zoox", "status": "Charging", "lat": 36.1584, "lng": -115.1452, "location": "Downtown Charging Station", "last_updated": "31 min ago", "speed": 0, "trips": 503},
    {"id": "ZOX-LV-078", "provider": "Zoox", "status": "Idle", "lat": 36.1402, "lng": -115.1321, "location": "Arts District", "last_updated": "22 min ago", "speed": 0, "trips": 76},
    {"id": "ZOX-LV-091", "provider": "Zoox", "status": "Active", "lat": 36.1523, "lng": -115.1498, "location": "Downtown Core", "last_updated": "Just now", "speed": 35, "trips": 142},
    {"id": "WAY-LV-007", "provider": "Waymo", "status": "Active", "lat": 36.1699, "lng": -115.1398, "location": "Downtown Fremont", "last_updated": "2 min ago", "speed": 22, "trips": 189},
    {"id": "WAY-LV-055", "provider": "Waymo", "status": "Active", "lat": 36.1335, "lng": -115.1649, "location": "The Sphere Area", "last_updated": "Just now", "speed": 31, "trips": 98},
    {"id": "WAY-LV-031", "provider": "Waymo", "status": "Active", "lat": 36.1028, "lng": -115.1812, "location": "Mandalay Bay", "last_updated": "4 min ago", "speed": 29, "trips": 154},
    {"id": "WAY-LV-014", "provider": "Waymo", "status": "Active", "lat": 36.1219, "lng": -115.1683, "location": "Planet Hollywood", "last_updated": "Just now", "speed": 18, "trips": 211},
    {"id": "WAY-LV-003", "provider": "Waymo", "status": "Active", "lat": 36.1758, "lng": -115.1187, "location": "Stratosphere Area", "last_updated": "6 min ago", "speed": 24, "trips": 389},
    {"id": "WAY-LV-112", "provider": "Waymo", "status": "Active", "lat": 36.0876, "lng": -115.1623, "location": "Near Airport", "last_updated": "3 min ago", "speed": 27, "trips": 267},
    {"id": "CYB-LV-001", "provider": "Cybercab", "status": "Active", "lat": 36.1205, "lng": -115.1752, "location": "Las Vegas Strip (Caesars)", "last_updated": "Just now", "speed": 32, "trips": 87},
    {"id": "CYB-LV-008", "provider": "Cybercab", "status": "Active", "lat": 36.1628, "lng": -115.1423, "location": "Downtown Las Vegas", "last_updated": "4 min ago", "speed": 19, "trips": 134},
    {"id": "CYB-LV-015", "provider": "Cybercab", "status": "Idle", "lat": 36.0854, "lng": -115.1489, "location": "Near Harry Reid Airport", "last_updated": "18 min ago", "speed": 0, "trips": 56},
    {"id": "CYB-LV-022", "provider": "Cybercab", "status": "Active", "lat": 36.1452, "lng": -115.1556, "location": "Arts District", "last_updated": "Just now", "speed": 27, "trips": 92},
]

PROVIDER_COLORS = {
    "Zoox": "#00f0ff",
    "Waymo": "#a855f7",
    "Cybercab": "#e82127",
}

STATUS_COLORS = {
    "Active": "🟢",
    "Idle": "🟡",
    "Charging": "🔵",
}


def init_session():
    if "vehicles" not in st.session_state:
        st.session_state.vehicles = [v.copy() for v in INITIAL_VEHICLES]
    if "last_update" not in st.session_state:
        st.session_state.last_update = datetime.now()
    if "auto_refresh" not in st.session_state:
        st.session_state.auto_refresh = True


def simulate_live_update():
    """Simulate movement and status changes for active vehicles."""
    vehicles = st.session_state.vehicles
    for v in vehicles:
        if v["status"] == "Active":
            v["lat"] += (random.random() - 0.5) * 0.004
            v["lng"] += (random.random() - 0.5) * 0.004
            v["lat"] = max(36.05, min(36.25, v["lat"]))
            v["lng"] = max(-115.25, min(-115.05, v["lng"]))
            v["speed"] = max(8, min(42, v["speed"] + (random.random() - 0.5) * 6))
            if random.random() < 0.25:
                v["trips"] += 1
            v["last_updated"] = "Just now"
        elif random.random() < 0.05:
            if v["status"] == "Idle" and random.random() < 0.3:
                v["status"] = "Active"
                v["speed"] = random.randint(15, 30)
                v["last_updated"] = "Just now"
    st.session_state.last_update = datetime.now()


def create_map(df):
    """Create Folium map centered on Las Vegas."""
    m = folium.Map(
        location=[36.15, -115.15],
        zoom_start=12,
        tiles="CartoDB dark_matter",
        control_scale=True,
    )

    for _, row in df.iterrows():
        color = PROVIDER_COLORS.get(row["provider"], "#ffffff")
        popup_html = f"""
        <div style="font-family: Inter, sans-serif; min-width: 180px;">
            <b style="font-size: 14px;">{row['id']}</b><br>
            <span style="color:{color}; font-weight:600;">{row['provider']}</span> • {row['status']}<br>
            📍 {row['location']}<br>
            🚀 {row['speed']} mph • 🚕 {row['trips']} trips<br>
            <small>Updated: {row['last_updated']}</small>
        </div>
        """
        folium.CircleMarker(
            location=[row["lat"], row["lng"]],
            radius=9 if row["status"] == "Active" else 6,
            color="#ffffff",
            weight=2,
            fill=True,
            fill_color=color,
            fill_opacity=0.9,
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"{row['id']} ({row['provider']})",
        ).add_to(m)

    return m


def main():
    init_session()

    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🤖 Vibe Robotaxi Tracker")
        st.caption("Live autonomous vehicle tracking • Las Vegas, NV • Pure Python Edition")
    with col2:
        st.write("")
        auto = st.toggle("🔴 LIVE Auto-Refresh", value=st.session_state.auto_refresh)
        st.session_state.auto_refresh = auto

    vehicles = st.session_state.vehicles
    df = pd.DataFrame(vehicles)

    active_count = len(df[df["status"] == "Active"])
    total_trips = df["trips"].sum()
    cybercab_trips = df[df["provider"] == "Cybercab"]["trips"].sum()
    total_spotted = len(df)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Active Vehicles", active_count)
    m2.metric("Total Spotted", total_spotted)
    m3.metric("Total Trips", f"{total_trips:,}")
    m4.metric("Cybercab Trips", f"{cybercab_trips:,}")

    st.divider()

    f1, f2, f3 = st.columns([1, 1, 2])
    with f1:
        provider_filter = st.selectbox("Provider", ["All", "Zoox", "Waymo", "Cybercab"], index=0)
    with f2:
        status_filter = st.selectbox("Status", ["All", "Active", "Idle", "Charging"], index=0)
    with f3:
        search = st.text_input("Search ID or Location", placeholder="e.g. ZOX-LV or Bellagio")

    filtered = df.copy()
    if provider_filter != "All":
        filtered = filtered[filtered["provider"] == provider_filter]
    if status_filter != "All":
        filtered = filtered[filtered["status"] == status_filter]
    if search:
        mask = (
            filtered["id"].str.contains(search, case=False, na=False)
            | filtered["location"].str.contains(search, case=False, na=False)
        )
        filtered = filtered[mask]

    left, right = st.columns([1.4, 1])

    with left:
        st.subheader("🗺️ Live Map • Las Vegas Metro")
        if not filtered.empty:
            m = create_map(filtered)
            st_folium(m, width=None, height=520, returned_objects=[])
        else:
            st.info("No vehicles match the current filters.")

    with right:
        st.subheader(f"📋 Live Registry  ({len(filtered)} vehicles)")
        display_df = filtered[["id", "provider", "status", "location", "speed", "trips", "last_updated"]].copy()
        display_df = display_df.rename(columns={
            "id": "ID",
            "provider": "Provider",
            "status": "Status",
            "location": "Location",
            "speed": "Speed (mph)",
            "trips": "Trips",
            "last_updated": "Updated",
        })
        st.dataframe(
            display_df,
            use_container_width=True,
            height=480,
            hide_index=True,
        )

    st.divider()
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        if st.button("🔄 Force Live Update", use_container_width=True):
            simulate_live_update()
            st.rerun()
    with c2:
        if st.button("➕ Submit Spotting", use_container_width=True):
            st.session_state.show_submit = True

    if st.session_state.get("show_submit", False):
        with st.form("submit_form"):
            st.subheader("Submit Live Spotting")
            sid = st.text_input("Vehicle ID", value="ZOX-LV-NEW")
            sprov = st.selectbox("Provider", ["Zoox", "Waymo", "Cybercab"])
            sstat = st.selectbox("Status", ["Active", "Idle", "Charging"])
            submitted = st.form_submit_button("Submit to Live Feed")
            if submitted:
                new_v = {
                    "id": sid,
                    "provider": sprov,
                    "status": sstat,
                    "lat": 36.15 + (random.random() - 0.5) * 0.08,
                    "lng": -115.15 + (random.random() - 0.5) * 0.08,
                    "location": "Newly spotted location",
                    "last_updated": "Just now",
                    "speed": random.randint(15, 30) if sstat == "Active" else 0,
                    "trips": random.randint(5, 40),
                }
                st.session_state.vehicles.append(new_v)
                st.session_state.show_submit = False
                st.success(f"Added {sid}!")
                st.rerun()

    # Real-time polling via streamlit-autorefresh (safe, no crash loops)
    if st.session_state.auto_refresh:
        # Refresh every 5 seconds
        count = st_autorefresh(interval=5000, key="live_refresh")
        if count > 0:
            simulate_live_update()
        st.caption(f"🔴 LIVE — auto-updating every 5s (refresh #{count})")
    else:
        st.caption("LIVE mode off — toggle above or click Force Live Update")


if __name__ == "__main__":
    main()
