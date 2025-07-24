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

# -- Caching Data Loading ------------------------------------------------
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

# -- Helpers ---------------------------------------------------------------

def filter_terms(df, label='Filter Fall Terms', key='filter_terms'):
    terms = sorted(df['Fall term'].unique())
    selected = st.sidebar.multiselect(label, terms, default=terms, key=key)
    return df[df['Fall term'].isin(selected)], selected

# -- App Configuration ----------------------------------------------------
st.set_page_config(page_title='UC Admissions Data Explorer', layout='wide')
st.title('📊 UC Admissions Data Explorer')
st.markdown('Explore trends in UC freshman applications by GPA, demographics, and acceptance rates.')

# -- Tabs Navigation ------------------------------------------------------
tab_gpa, tab_demo, tab_accept, tab_raw = st.tabs([
    'GPA Distribution',
    'Demographics',
    'Acceptance Rate',
    'Raw Data'
])

# -- GPA Distribution Tab ------------------------------------------------
with tab_gpa:
    st.subheader('📈 GPA Distribution Over Time')
    df_gpa, years = filter_terms(get_gpa_df(), key='gpa_terms')
    fig = plot_gpa_distribution(df_gpa, terms=years)
    st.pyplot(fig)

# -- Demographics Tab -----------------------------------------------------
with tab_demo:
    st.subheader('👥 Applicants by Race/Ethnicity')
    df_demo, years = filter_terms(get_demo_df(), key='demo_terms')
    groups = sorted(df_demo['Race/ethnicity'].unique())
    selected_groups = st.sidebar.multiselect(
        'Filter Ethnicities', groups, default=groups, key='ethnicity_groups'
    )
    df_demo = df_demo[df_demo['Race/ethnicity'].isin(selected_groups)]
    fig = plot_demographics_distribution(df_demo, terms=years, groups=selected_groups)
    st.pyplot(fig)

# -- Acceptance Rate Tab -------------------------------------------------
with tab_accept:
    st.subheader('📊 Acceptance Rate Over Time')
    df_acc, years = filter_terms(get_app_admit_df(), key='acceptance_terms')
    fig = plot_acceptance_rate(df_acc, terms=years)
    st.pyplot(fig)

# -- Raw Data Tab ---------------------------------------------------------
with tab_raw:
    st.subheader('📄 Raw Dataset Preview & Download')
    choice = st.selectbox(
        'Choose a dataset',
        ['GPA', 'Demographics', 'Applications', 'Applications + Admits'],
        key='raw_choice'
    )
    if choice == 'GPA':
        df = get_gpa_df()
    elif choice == 'Demographics':
        df = get_demo_df()
    elif choice == 'Applications':
        df = get_frosh_app_df()
    else:
        df = get_app_admit_df()
    st.dataframe(df, use_container_width=True)
    csv = df.to_csv(index=False)
    st.download_button(
        label='Download as CSV',
        data=csv,
        file_name=f'{choice.lower().replace(' ', '_')}.csv',
        mime='text/csv',
        key='download_button'
    )
