import pandas as pd
import os


def load_and_clean_frosh_app_counts(filepath=None):
    """
    Load and clean frosh application counts data.
    """
    if filepath is None:
        base = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(base, '..', 'data', 'frosh_app_counts.csv')
    df = pd.read_csv(filepath, encoding='utf-16', sep='\t')
    df.dropna(how='all', inplace=True)
    df.rename(columns={'Residency': 'Applicants'}, inplace=True)
    df['Applicants'] = df['Applicants'].astype(str).str.replace(',', '').astype(int)
    return df


def load_and_clean_gpa_distribution(filepath=None):
    """
    Load and clean GPA distribution data.
    """
    if filepath is None:
        base = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(base, '..', 'data', 'frosh_avg_gpa.csv')
    df = pd.read_csv(filepath, encoding='utf-16', sep='\t')
    df.columns = df.columns.str.strip()
    df.dropna(how='all', inplace=True)
    df.rename(columns={
        'HS weighted, capped GPA': 'Applicants',
        'Applicant characteristics': 'GPA Band'
    }, inplace=True)
    df['Applicants'] = df['Applicants'].astype(str).str.replace(',', '').astype(int)
    return df


def load_and_clean_ethnicity_data(filepath=None):
    """
    Load and clean ethnicity distribution data.
    """
    if filepath is None:
        base = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(base, '..', 'data', 'frosh_ethnicity.csv')
    df = pd.read_csv(filepath, encoding='utf-16', sep='\t')
    df.columns = df.columns.str.strip()
    df.dropna(how='all', inplace=True)
    df.rename(columns={
        'Applicant characteristics': 'Race/ethnicity',
        'Race/ethnicity': 'Applicants'
    }, inplace=True)
    df['Applicants'] = df['Applicants'].astype(str).str.replace(',', '').astype(int)
    return df

