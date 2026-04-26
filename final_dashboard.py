import streamlit as st
import pandas as pd

st.title("Freedom In World Dashboard")

st.header("Exploring countries political rights and civil liberties globally")

st.markdown("""
            <style>
            .stApp {
            background-color: #2b2b2b;
            color: white;
            }
            [data-testid = "stMetricValue"] {
            color: white}
            [data-testid = "stMetricLabel"] {
            color :white}
            </style>
""", unsafe_allow_html = True)

df = pd.read_csv("cleaned_freedom_dataset.csv")

df["OBS_VALUE"] = pd.to_numeric(df["OBS_VALUE"], errors= "coerce" )
df["TIME_PERIOD"] = df["TIME_PERIOD"].astype(int)

st.sidebar.header("Filter")

year = st.sidebar.slider("Select the year",
    int(df["TIME_PERIOD"].min()),
    int(df["TIME_PERIOD"].max()),
    2020)

indicators = df["INDICATOR_LABEL"].unique().tolist()
indicator_select = st.sidebar.selectbox("Choose an indicator", indicators)

filtered = df[
    (df["TIME_PERIOD"] == year) &
    (df["INDICATOR_LABEL"] == indicator_select)
]

st.subheader(f"Raw Data ({year})")
st.dataframe(filtered[["REF_AREA_LABEL", "OBS_VALUE"]].rename(columns={
    "REF_AREA_LABEL": "Country",
    "OBS_VALUE": "Score"
}).reset_index(drop=True))

st.subheader(f"Global Stats ({year})")

col1, col2, col3 = st.columns(3)

col1.metric("Global Average", round(filtered["OBS_VALUE"].mean(), 2))
col2.metric("Highest Score", filtered["OBS_VALUE"].max())
col3.metric("Lowest Score", filtered["OBS_VALUE"].min())

st.subheader(f"Top 10 Countries by Indicator ({year})")
top10 = filtered.nlargest(10, "OBS_VALUE")[["REF_AREA_LABEL", "OBS_VALUE"]].set_index("REF_AREA_LABEL")
st.bar_chart(top10)

st.subheader("Country Trend Over Time")
countries = sorted(df["REF_AREA_LABEL"].unique().tolist())
selected_country = st.selectbox("Select a country", countries)

trend = df[
    (df["REF_AREA_LABEL"] == selected_country) &
    (df["INDICATOR_LABEL"] == indicator_select)
].copy()

trend["TIME_PERIOD"] = trend["TIME_PERIOD"].astype(str)
trend = trend[["TIME_PERIOD", "OBS_VALUE"]].set_index("TIME_PERIOD")

st.line_chart(trend)

st.subheader(f"Global Stats ({year})")

st.subheader("Compare Two Countries")

col1, col2 = st.columns(2)
country1 = col1.selectbox("Select first country", countries, key="country1")
country2 = col2.selectbox("Select second country", countries, key="country2")

country1_data = df[
    (df["REF_AREA_LABEL"] == country1) &
    (df["INDICATOR_LABEL"] == indicator_select)
].copy()
country1_data["TIME_PERIOD"] = country1_data["TIME_PERIOD"].astype(str)
country1_data = country1_data[["TIME_PERIOD", "OBS_VALUE"]].set_index("TIME_PERIOD").rename(columns={"OBS_VALUE": country1})

country2_data = df[
    (df["REF_AREA_LABEL"] == country2) &
    (df["INDICATOR_LABEL"] == indicator_select)
].copy()
country2_data["TIME_PERIOD"] = country2_data["TIME_PERIOD"].astype(str)
country2_data = country2_data[["TIME_PERIOD", "OBS_VALUE"]].set_index("TIME_PERIOD").rename(columns={"OBS_VALUE": country2})

compare = country1_data.join(country2_data, lsuffix="_1", rsuffix="_2")
st.line_chart(compare)