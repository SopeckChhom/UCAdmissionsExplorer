import matplotlib.pyplot as plt
import pandas as pd

def plot_gpa_distribution(df: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(12, 6))
    df.groupby(['Fall term','GPA Band'])['Applicants']\
      .sum()\
      .unstack()\
      .plot(kind='bar', stacked=True, ax=ax)
    ax.set_ylabel('Applicants')
    ax.set_xlabel('Fall Term')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    fig.tight_layout()
    return fig

def plot_demographics_distribution(df: pd.DataFrame) -> plt.Figure:
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
    return fig
