import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load dataset
file_path = "Indicators_NHO Nov 2020.csv"
df = pd.read_csv(file_path)

# Clean and process data
df = df.dropna(subset=["years", "Data", "Indicator", "Category", "Levelname"])
df["years"] = df["years"].astype(int)
df["Level"] = df["Level"].str.lower()

# Define Rwanda-themed color palette
rwanda_colors = ["#1B5E20", "#FFD700", "#00A2E8", "#F9A825"]  # Green, Gold, Blue, and Yellow

# Dictionary with approximate lat/lon coordinates for Rwanda districts
district_coords = {
    "Kigali": (-1.9536, 30.0605), "Gasabo": (-1.9499, 30.1127), "Nyarugenge": (-1.9416, 30.0617),
    "Kicukiro": (-1.9781, 30.1395), "Huye": (-2.5967, 29.7401), "Musanze": (-1.4995, 29.6351),
    "Rubavu": (-1.6751, 29.2611), "Rusizi": (-2.5323, 28.8993), "Nyagatare": (-1.3097, 30.3249),
    "Rwamagana": (-1.9496, 30.4346), "Muhanga": (-2.0636, 29.7471), "Bugesera": (-2.2008, 30.1519)
}

# Streamlit App
st.set_page_config(page_title="Health Indicators Dashboard", layout="wide")
st.title("📊 Health Indicators Insights Dashboard")
st.markdown("Gain insights into key health indicators across different geographic levels: **National, Provincial, and District.**")

# Sidebar Category Selection
category = st.sidebar.selectbox("📂 Select a Category", df["Category"].unique())
df_category = df[df["Category"] == category]

# Sidebar Indicator Selection
indicator = st.sidebar.selectbox("📊 Select an Indicator", df_category["Indicator"].unique())
df_selected = df_category[df_category["Indicator"] == indicator]

st.header(f"🔎 Exploring {indicator} in {category}")
st.write("This section provides an overview of the selected indicator with dynamic visualizations.")

# National Level Analysis
st.subheader("🌍 National Trends Over Time")
national_data = df_selected[df_selected["Level"] == "national"]
if not national_data.empty:
    national_agg = national_data.groupby("years")["Data"].mean().reset_index()
    fig_national = px.line(national_agg, x="years", y="Data", markers=True, title=f"📈 {indicator} Trend at National Level",
                            line_shape='spline', color_discrete_sequence=[rwanda_colors[2]])
    fig_national.update_traces(line=dict(width=3), marker=dict(size=10, symbol="circle", opacity=0.8))
    st.plotly_chart(fig_national, use_container_width=True)
    st.write("This graph illustrates how the indicator has evolved over time at the **National Level**.")
else:
    st.write("❌ No data available at the national level.")

# Province Level Analysis
st.subheader("🏢 Provincial Comparisons")
province_data = df_selected[df_selected["Level"] == "province"]
if not province_data.empty:
    province_agg = province_data.groupby(["Levelname"])["Data"].mean().reset_index()
    fig_province = px.bar(province_agg, x="Levelname", y="Data", color="Levelname", title=f"🏛 {indicator} Across Provinces",
                           color_discrete_sequence=[rwanda_colors[1]])
    fig_province.update_traces(marker=dict(line=dict(width=1)), opacity=0.8)
    st.plotly_chart(fig_province, use_container_width=True)
    st.write("This **bar chart** highlights provincial-level differences in the selected health indicator.")
else:
    st.write("❌ No provincial data available.")

# District Level Analysis
st.subheader("🏘️ District-Level Insights")
district_data = df_selected[df_selected["Level"] == "district"]
if not district_data.empty:
    district_agg = district_data.groupby(["Levelname"])["Data"].mean().reset_index()
    fig_district = px.bar(district_agg, x="Levelname", y="Data", color="Levelname", title=f"🏠 {indicator} Across Districts",
                           color_discrete_sequence=[rwanda_colors[0]])
    fig_district.update_traces(marker=dict(line=dict(width=1)), opacity=0.8)
    st.plotly_chart(fig_district, use_container_width=True)
    st.write("This **district-level analysis** provides a localized perspective on the indicator.")
else:
    st.write("❌ No district-level data available.")

# Map Visualization (Scatter Mapbox)
st.subheader("🗺️ Rwanda Map Visualization")
if not df_selected.empty:
    df_selected["lat"] = df_selected["Levelname"].map(lambda x: district_coords.get(x, (None, None))[0])
    df_selected["lon"] = df_selected["Levelname"].map(lambda x: district_coords.get(x, (None, None))[1])
    df_selected = df_selected.dropna(subset=["lat", "lon"])
    
    fig_map = px.scatter_mapbox(
        df_selected, lat="lat", lon="lon", size="Data", color="Data",
        hover_data={"Levelname": False, "lat": False, "lon": False, "Data": True},
        title=f"{indicator} Across Rwanda's Districts",
        color_continuous_scale=[rwanda_colors[2], rwanda_colors[1], rwanda_colors[0]],
        mapbox_style="carto-positron",
        zoom=7, center={"lat": -1.9403, "lon": 29.8739}
    )
    fig_map.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)
    st.write("This **map visualization** provides a geographical perspective on the indicator's distribution across districts.")
else:
    st.write("❌ No geographic data available for mapping.")

# Summary Statistics
st.subheader("📊 Key Insights & Statistics")
st.write("Below is a statistical summary of the selected indicator across different levels.")
st.dataframe(df_selected.groupby("Level")["Data"].describe().T)
