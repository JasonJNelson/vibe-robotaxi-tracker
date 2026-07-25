# Vibe Robotaxi Tracker - Las Vegas

Live autonomous vehicle tracking dashboard for **Zoox**, **Waymo** & **Cybercab** in Las Vegas.

## Two versions included

### 1. Pure Python (Streamlit) – Recommended
```bash
pip install -r requirements_streamlit.txt
streamlit run robotaxi_tracker.py
```
Open http://localhost:8501

### 2. Original HTML + WebSocket server
```bash
python server.py          # Terminal 1
# Then open VibeRobotaxi_Tracker_Fixed.html in browser
```

## Features
- Live map with Folium / Leaflet
- Real-time vehicle movement simulation
- Provider filters (Zoox / Waymo / Cybercab)
- Searchable registry table
- Submit new sightings
- Auto-refresh

## Deploy
- Streamlit: Streamlit Cloud or Hugging Face Spaces
- HTML version: GitHub Pages + Render for the WebSocket backend

Built for Las Vegas robotaxi enthusiasts.
