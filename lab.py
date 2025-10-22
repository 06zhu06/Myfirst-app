import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
st.set_page_config(page_title="California Housing (1990)", layout="wide")
st.title("California Housing Data (1990)")
st.markdown("**by Hanglin Zhu**")   
df = pd.read_csv("housing.csv")
st.sidebar.header("See more filters in the sidebar:")
min_price, max_price = int(df.median_house_value.min()), int(df.median_house_value.max())
price_range = st.sidebar.slider(
    "Minimal Median House Price", 0, 500001, (min_price, max_price)
)
location_options = df.ocean_proximity.unique()
selected_locations = st.sidebar.multiselect(
    "Select location type",
    options=location_options,
    default=location_options
)
income_map = {"Low": (0, 2.5), "Medium": (2.5, 4.5), "High": (4.5, 50)}
income_level = st.sidebar.radio("Income level", options=list(income_map.keys()))
low, high = income_map[income_level]
mask = (
    (df.median_house_value >= price_range[0])
    & (df.median_house_value <= price_range[1])
    & (df.ocean_proximity.isin(selected_locations))
    & (df.median_income >= low)
    & (df.median_income < high)
)
filtered = df[mask]
st.sidebar.markdown(f"**{len(filtered)}** rows selected")

st.subheader("Geographic distribution")
if not filtered.empty:
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=filtered,
        get_position=["longitude", "latitude"],
        get_radius=200,
        get_fill_color=["median_house_value / 500000 * 255", 140, 180],
        pickable=True,
    )
    view_state = pdk.ViewState(
        latitude=filtered.latitude.mean(),
        longitude=filtered.longitude.mean(),
        zoom=5,
        pitch=0,
    )
    r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{median_house_value}"})
    st.pydeck_chart(r)
else:
    st.warning("No data matches the current filters.")
st.subheader("Histogram of Median House Value")
fig, ax = plt.subplots()
ax.hist(filtered["median_house_value"], bins=30, color="skyblue", edgecolor="black")
ax.set_xlabel("Median House Value")
ax.set_ylabel("Count")
st.pyplot(fig)
