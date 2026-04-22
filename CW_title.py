import streamlit as st
import pandas as pd

st.title("Freedom In World Dashboard")

st.header("Exploring countries political rights and civil liberties globally")

df = pd.read_csv("cleaned_freedom_dataset.csv")

