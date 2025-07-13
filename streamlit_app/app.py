# streamlit_app/app.py

import streamlit as st
import pandas as pd
import os, sys
sys.path.append(os.path.abspath('./scripts'))

from clean_data import (
    load_and_clean_frosh_app_counts,
    load_and_clean_gpa_distribution,
    load_and_clean_ethnicity_data
)
from visualize import plot_gpa_distribution, plot_demographics_distribution


st.set_page_config(page_title="UC Admissions Data Explorer", layout="wide")

st.title("📊 UC Admissions Data Explorer")
st.markdown("Explore trends in UC freshman applications by GPA, demographics, and more.")

# Sidebar navigation
page = st.sidebar.radio("Select View", ["GPA Distribution", "Demographics", "Raw Data"])

# GPA Distribution View
if page == "GPA Distribution":
    df_gpa = load_and_clean_gpa_distribution()

    st.subheader("📈 GPA Distribution Over Time")
    fig = plot_gpa_distribution(df_gpa)
    st.pyplot(fig)


# Demographics View
elif page == "Demographics":
    df_eth = load_and_clean_ethnicity_data()

    st.subheader("👥 Applicants by Race/Ethnicity")
    fig = plot_demographics_distribution(df_eth)
    st.pyplot(fig)

# Raw Data Viewer
elif page == "Raw Data":
    st.subheader("📄 Raw Dataset Preview")
    dataset = st.selectbox("Choose a dataset", ["GPA", "Demographics", "Applications"])
    
    if dataset == "GPA":
        df = load_and_clean_gpa_distribution()
    elif dataset == "Demographics":
        df = load_and_clean_ethnicity_data()
    else:
        df = load_and_clean_frosh_app_counts()

    st.dataframe(df)

