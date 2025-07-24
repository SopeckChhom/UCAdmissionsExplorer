import matplotlib.pyplot as plt
import pandas as pd
import os

# Determine and create the plot directory
PLOT_DIR = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'plots')
os.makedirs(PLOT_DIR, exist_ok=True)

# plot gpa
def plot_gpa_distribution(df: pd.DataFrame, terms: list[str] = None, gpa_bands: list[str] = None) -> plt.Figure:
    #FIlter if args provided
    if terms is not None:
        df = df[df['Fall term'].isin(terms)]
    if gpa_bands is not None:
        df = df[df['GPA BAND'].isin(gpa_bands)]

    # plots
    fig, ax = plt.subplots(figsize=(12, 6))
    df.groupby(['Fall term','GPA Band'])['Applicants']\
      .sum()\
      .unstack()\
      .plot(kind='bar', stacked=True, ax=ax)
    ax.set_ylabel('Applicants')
    ax.set_xlabel('Fall Term')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    fig.tight_layout()

    #save
    out_path = os.path.join(PLOT_DIR, 'gpa_distribution.png')
    fig.savefig(out_path, bbox_inches='tight')

    return fig

# plot demographics
def plot_demographics_distribution(df: pd.DataFrame, terms: list[str] = None, groups: list[str] = None) -> plt.Figure:
    #FIlter if args provided
    if terms is not None:
        df = df[df['Fall term'].isin(terms)]
    if groups is not None:
        df = df[df['Race/ethnicity'].isin(groups)]
    df_pct = df.copy()
    df_pct['Total'] = df_pct.groupby('Fall term')['Applicants'].transform('sum')
    df_pct['Percentage'] = df_pct['Applicants']/df_pct['Total']*100

    fig, ax = plt.subplots(figsize=(12, 6))
    df_pct.pivot(index='Fall term',
                 columns='Race/ethnicity',
                 values='Percentage')\
          .plot(kind='bar', stacked=True, ax=ax)
    ax.set_ylabel('% of Applicants')
    ax.set_xlabel('Fall Term')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    fig.tight_layout()

    # save
    out_path = os.path.join(PLOT_DIR, 'demographics_distribution.png')
    fig.savefig(out_path, bbox_inches='tight')

    return fig

def plot_acceptance_rate(
    df: pd.DataFrame, 
    terms: list[str] = None
) -> plt.Figure:
    # 1) Optional term filter
    if terms is not None:
        df = df[df['Fall term'].isin(terms)]

    # 2) Aggregate totals
    agg = df.groupby('Fall term')[['Applicants', 'Admits']].sum()
    agg['Acceptance Rate'] = agg['Admits'] / agg['Applicants'] * 100

    # 3) Plot
    fig, ax = plt.subplots(figsize=(12, 6))
    agg['Acceptance Rate'].plot(marker='o', ax=ax)
    ax.set_ylabel('Acceptance Rate (%)')
    ax.set_xlabel('Fall Term')
    ax.set_xticklabels(agg.index, rotation=0)
    fig.tight_layout()

    # 4) Save
    out_path = os.path.join(PLOT_DIR, 'acceptance_rate.png')
    fig.savefig(out_path, bbox_inches='tight')
    return fig
