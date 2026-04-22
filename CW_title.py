import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Freedom In World Dashboard")

st.header("Exploring countries political rights and civil liberties globally")

df = pd.read_csv("cleaned_freedom_dataset.csv")

