# streamlit_app/app.py

import streamlit as st
import sys
from pathlib import Path

# Point to your scripts folder for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT / 'scripts'))

from clean_data import (
    load_and_clean_frosh_app_counts,
    load_and_clean_gpa_distribution,
    load_and_clean_ethnicity_data,
    load_and_clean_app_and_admit_counts
)
from visualize import (
    plot_gpa_distribution,
    plot_demographics_distribution,
    plot_acceptance_rate
)

# Caching Data Loading
@st.cache_data
def get_gpa_df():
    return load_and_clean_gpa_distribution()

@st.cache_data
def get_demo_df():
    return load_and_clean_ethnicity_data()

@st.cache_data
def get_app_admit_df():
    return load_and_clean_app_and_admit_counts()

@st.cache_data
def get_frosh_app_df():
    return load_and_clean_frosh_app_counts()

# Helpers 
def filter_terms(df, label='Filter Fall Terms', key='filter_terms'):
    terms = sorted(df['Fall term'].unique())
    selected = st.sidebar.multiselect(label, terms, default=terms, key=key)
    return df[df['Fall term'].isin(selected)], selected

# App Configuration
st.set_page_config(page_title='UC Admissions Data Explorer', layout='wide')
st.title('📊 UC Admissions Data Explorer')
st.markdown('Explore trends in UC freshman applications by GPA, demographics, and acceptance rates.')

# Tabs Navigation
st.sidebar.header("Filters")
tab_gpa, tab_demo, tab_accept, tab_raw = st.tabs([
    'GPA Distribution',
    'Demographics',
    'Acceptance Rate',
    'Raw Data'
])

# GPA Distribution Tab
with tab_gpa:
    st.subheader('📈 GPA Distribution Over Time')
    df_gpa = get_gpa_df()
    years = sorted(df_gpa['Fall term'].unique())
    year_range = st.slider("Select Year Range", min_value=min(years), max_value=max(years), value=(min(years), max(years)), step=1, key='gpa_year_range')
    df_gpa = df_gpa[df_gpa['Fall term'].between(*year_range)]
    fig = plot_gpa_distribution(df_gpa, terms=list(range(*year_range)) if year_range[0] != year_range[1] else [year_range[0]])
    st.plotly_chart(fig, use_container_width=True)

# Demographics Tab
with tab_demo:
    df_demo = get_demo_df()
    years = sorted(df_demo['Fall term'].unique())
    year_range = st.slider("Select Year Range", min_value=min(years), max_value=max(years), value=(min(years), max(years)), step=1, key='demo_year_range')
    df_demo = df_demo[df_demo['Fall term'].between(*year_range)]

    groups = sorted(df_demo['Race/ethnicity'].unique())
    selected_groups = st.sidebar.multiselect('Filter Ethnicities', groups, default=groups, key='ethnicity_groups')
    df_demo = df_demo[df_demo['Race/ethnicity'].isin(selected_groups)]

    fig = plot_demographics_distribution(df_demo, terms=list(range(*year_range)) if year_range[0] != year_range[1] else [year_range[0]],groups=selected_groups)
    st.plotly_chart(fig, use_container_width=True)

# Acceptance Rate Tab 
with tab_accept:
    st.subheader('📊 Acceptance Rate Over Time')
    df = get_app_admit_df()
    years = sorted(df['Fall term'].unique())
    year_range = st.slider(
    "Select Year Range:",
    min_value=min(years),
    max_value=max(years),
    value=(min(years), max(years)),
    step=1
    )
    df_acc = df[df['Fall term'].between(*year_range)]
    selected_years = df_acc['Fall term'].unique().tolist()
    fig = plot_acceptance_rate(df_acc, terms=selected_years)

    fig = plot_acceptance_rate(df_acc, terms=years)
    st.plotly_chart(fig, use_container_width=True)

    st.caption("📉 **2020:** Dip due to COVID-19.")
    st.caption("📈 **2024:** Record-high admits across the UC system.")

# Raw Data Tab 
with tab_raw:
    st.subheader('📄 Raw Dataset Preview & Download')
    choice = st.selectbox(
        'Choose a dataset',
        ['GPA', 'Demographics', 'Applications', 'Applications + Admits'],
        key='raw_choice'
    )
    data_options = {
    'GPA': get_gpa_df,
    'Demographics': get_demo_df,
    'Applications': get_frosh_app_df,
    'Applications + Admits': get_app_admit_df
    }
    df = data_options[choice]()

    st.dataframe(df, use_container_width=True)
    csv = df.to_csv(index=False)
    st.download_button(
        label='Download as CSV',
        data=csv,
        file_name=f'{choice.lower().replace(' ', '_')}.csv',
        mime='text/csv',
        key='download_button'
    )
