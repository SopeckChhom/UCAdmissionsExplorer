import matplotlib.pyplot as plt
import plotly.express as px
from typing import Optional
import pandas as pd
import os

# Determine and create the plot directory
PLOT_DIR = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'plots')
os.makedirs(PLOT_DIR, exist_ok=True)

# plot gpa
def plot_gpa_distribution(
    df: pd.DataFrame,
    terms: Optional[list[str]] = None,
    gpa_bands: Optional[list[str]] = None
):
    if terms is not None:
        df = df[df['Fall term'].isin(terms)]
    if gpa_bands is not None:
        df = df[df['GPA Band'].isin(gpa_bands)]

    # Group by term and GPA band
    agg = df.groupby(['Fall term', 'GPA Band'])['Applicants'].sum().reset_index()

    fig = px.bar(
        agg,
        x='Fall term',
        y='Applicants',
        color='GPA Band',
        title='GPA Distribution of Applicants Over Time',
        labels={'Applicants': 'Number of Applicants'},
        barmode='stack',
        hover_data={'Applicants': True, 'GPA Band': True},
    )

    fig.update_layout(
        xaxis_title="Fall Term",
        yaxis_title="Applicants",
        legend_title="GPA Band"
    )
    if os.getenv("EXPORT_MODE") == "true":
        fig.write_image("outputs/plots/gpa_distribution_plotly.png")

    return fig

# plot demographics
def plot_demographics_distribution(
    df: pd.DataFrame,
    terms: Optional[list[str]] = None,
    groups: Optional[list[str]] = None
):
    if terms is not None:
        df = df[df['Fall term'].isin(terms)]
    if groups is not None:
        df = df[df['Race/ethnicity'].isin(groups)]

    df_pct = df.copy()
    df_pct['Total'] = df_pct.groupby('Fall term')['Applicants'].transform('sum')
    df_pct['Percentage'] = df_pct['Applicants'] / df_pct['Total'] * 100

    fig = px.bar(
        df_pct,
        x='Fall term',
        y='Percentage',
        color='Race/ethnicity',
        barmode='stack',
        title='Demographics of Applicants Over Time',
        hover_data={
            'Applicants': True,
            'Race/ethnicity': True,
            'Percentage': ':.2f'
        },
        labels={'Percentage': '% of Applicants'}
    )

    fig.update_layout(
        xaxis_title="Fall Term",
        yaxis_title="% of Applicants",
        yaxis_tickformat=".0%",
        legend_title="Race/Ethnicity"
    )

    return fig

def plot_acceptance_rate(
    df: pd.DataFrame, 
    terms: Optional[list[str]] = None
):
    if terms is not None:
        df = df[df['Fall term'].isin(terms)]

    # Aggregate totals
    agg = df.groupby('Fall term')[['Applicants', 'Admits']].sum().reset_index()
    agg['Acceptance Rate'] = agg['Admits'] / agg['Applicants']

    # Plotly line chart
    fig = px.line(
        agg,
        x='Fall term',
        y='Acceptance Rate',
        markers=True,
        hover_data={
            'Fall term': True,
            'Applicants': True,
            'Admits': True,
            'Acceptance Rate': ':.2%'  
        },
        title='UC Freshman Acceptance Rate Over Time'
    )

    fig.update_layout(
        yaxis_tickformat=".0%",
        xaxis_title="Fall Term",
        yaxis_title="Acceptance Rate",
        hovermode="x unified"
    )

    return fig
