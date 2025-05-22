import altair as alt
import pandas as pd
import requests
import streamlit as st

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="VPP Dashboard", layout="wide")
st.title("🔋 Virtual Power Plant Dashboard")

# Sidebar: Plant registration form
st.sidebar.header("Register New Plant")
with st.sidebar.form("register_form"):
    name = st.text_input("Name")
    max_capacity = st.number_input("Max Capacity (kW)", min_value=0.0, format="%.2f")
    min_capacity = st.number_input("Min Capacity (kW)", min_value=0.0, format="%.2f")
    status = st.selectbox("Status", ["idle", "running", "down"])
    submit = st.form_submit_button("Register")
    if submit:
        payload = {
            "id": 0,
            "name": name,
            "max_capacity": max_capacity,
            "min_capacity": min_capacity,
            "status": status,
        }
        resp = requests.post(f"{API_BASE}/plants/", json=payload)
        if resp.status_code == 200:
            st.sidebar.success("Plant registered!")
            st.cache_data.clear()
        else:
            st.sidebar.error(f"Error: {{resp.text}}")


@st.cache_data(ttl=60)
def load_plants():
    r = requests.get(f"{API_BASE}/plants/")
    data = r.json()
    return pd.DataFrame(data)


# Load plant data
plants_df = load_plants()

# If no plants, show info
if plants_df.empty:
    st.info("No plants registered yet. Use the form in the sidebar to add plants.")
    st.stop()

# Main dashboard
total_capacity = plants_df.query("status != 'down'")["max_capacity"].sum()
st.metric("⚡ Total Available Capacity (kW)", f"{total_capacity:.0f}")

# Bar chart of capacities
cap_chart = (
    alt.Chart(plants_df)
    .mark_bar()
    .encode(
        x=alt.X("name:N", title="Plant"),
        y=alt.Y("max_capacity:Q", title="Max Capacity (kW)"),
        color=alt.Color("status:N", legend=alt.Legend(title="Status")),
    )
    .properties(width=700, height=300)
)
st.subheader("Plant Capacities")
st.altair_chart(cap_chart, use_container_width=True)

# Dispatch slider (never allow 0)
if total_capacity <= 0:
    st.warning("No available capacity to dispatch.")
    st.stop()

# Compute max & default demand
max_demand = max(int(total_capacity * 1.5), 1)
default_demand = min(max(int(total_capacity * 0.8), 1), max_demand)

# If only one possible value, use number_input instead of slider
if max_demand == 1:
    demand = st.sidebar.number_input(
        "Set demand (kW)",
        min_value=1,
        max_value=1,
        value=1,
        help="Only 1 kW possible given current capacity",
    )
else:
    demand = st.sidebar.slider(
        "Set demand (kW)",
        min_value=1,
        max_value=max_demand,
        value=default_demand,
        help="Adjust to set how much demand to dispatch",
    )
st.subheader(f"Dispatch Allocation for Demand = {demand} kW")
resp = requests.post(f"{API_BASE}/dispatch/", json={"demand": demand})
if not resp.ok:
    st.error(f"Dispatch failed: {resp.status_code} – {resp.text}")
    st.stop()

data = resp.json()
allocations = data.get("allocations", {})
alloc = pd.DataFrame(resp.json()["allocations"].items(), columns=["id", "allocated"])

alloc["id"] = alloc["id"].astype(int)

alloc = alloc.merge(plants_df[["id", "name"]], on="id").set_index("name")

# Allocation table
st.table(alloc)

# Pie chart of allocation
pie = (
    alt.Chart(alloc.reset_index())
    .mark_arc(innerRadius=50)
    .encode(
        theta=alt.Theta("allocated:Q", title="Allocated kW"),
        color=alt.Color("name:N", legend=alt.Legend(title="Plant")),
    )
    .properties(width=300, height=300)
)
st.altair_chart(pie, use_container_width=False)
