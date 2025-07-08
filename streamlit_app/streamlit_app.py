# streamlit_app.py

import streamlit as st
import pandas as pd
import os
import sys

# Load cleaning functions
sys.path.append(os.path.abspath('./scripts'))
from clean_data import (
    load_and_clean_frosh_app_counts,
    load_and_clean_gpa_distribution,
    load_and_clean_ethnicity_data
)

st.set_page_config(page_title="UC Admissions Data Explorer", layout="wide")

st.title("📊 UC Admissions Data Explorer")
st.markdown("Explore trends in UC freshman applications by GPA, demographics, and more.")

# Sidebar navigation
page = st.sidebar.radio("Select View", ["GPA Distribution", "Demographics", "Raw Data"])

# GPA Distribution View
if page == "GPA Distribution":
    df_gpa = load_and_clean_gpa_distribution()

    st.subheader("📈 GPA Distribution Over Time")
    df_pct = df_gpa.copy()
    total_by_year = df_pct.groupby('Fall term')['Applicants'].transform('sum')
    df_pct['Percentage'] = df_pct['Applicants'] / total_by_year * 100
    chart_data = df_pct.pivot(index='Fall term', columns='GPA Band', values='Percentage')

    st.bar_chart(chart_data)

# Demographics View
elif page == "Demographics":
    df_eth = load_and_clean_ethnicity_data()

    st.subheader("👥 Applicants by Race/Ethnicity")
    df_pct = df_eth.copy()
    total = df_pct.groupby('Fall term')['Applicants'].transform('sum')
    df_pct['Percentage'] = df_pct['Applicants'] / total * 100
    chart_data = df_pct.pivot(index='Fall term', columns='Race/ethnicity', values='Percentage')

    st.bar_chart(chart_data)

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

