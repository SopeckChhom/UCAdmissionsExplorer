import os
import pandas as pd

# Project directories
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
CLEANED_DIR = os.path.join(BASE_DIR, 'data', 'cleaned')


def load_and_clean_frosh_app_counts(filepath: str = None) -> pd.DataFrame:
    """
    Load and clean frosh application counts data.
    Returns columns: ['Fall term', 'Applicant characteristics', 'Applicants']
    """
    if filepath is None:
        filepath = os.path.join(RAW_DIR, 'frosh_app_counts.csv')
    df = pd.read_csv(filepath, encoding='utf-16', sep='\t')
    df.columns = df.columns.str.strip()
    df.dropna(how='all', inplace=True)
    df.rename(columns={'Residency': 'Applicants'}, inplace=True)
    df['Applicants'] = (
        df['Applicants']
        .astype(str)
        .str.replace(',', '')
        .astype(int)
    )
    return df[['Fall term', 'Applicant characteristics', 'Applicants']]


def load_and_clean_gpa_distribution(filepath: str = None) -> pd.DataFrame:
    """
    Load and clean GPA distribution data.
    Returns columns: ['Fall term', 'GPA Band', 'Applicants']
    """
    if filepath is None:
        filepath = os.path.join(RAW_DIR, 'frosh_avg_gpa.csv')
    df = pd.read_csv(filepath, encoding='utf-16', sep='\t')
    df.columns = df.columns.str.strip()
    df.dropna(how='all', inplace=True)
    df.rename(columns={
        'Applicant characteristics': 'GPA Band',
        'HS weighted, capped GPA': 'Applicants'
    }, inplace=True)
    df['Applicants'] = (
        df['Applicants']
        .astype(str)
        .str.replace(',', '')
        .astype(int)
    )
    return df[['Fall term', 'GPA Band', 'Applicants']]


def load_and_clean_ethnicity_data(filepath: str = None) -> pd.DataFrame:
    """
    Load and clean ethnicity distribution data.
    Returns columns: ['Fall term', 'Race/ethnicity', 'Applicants']
    """
    if filepath is None:
        filepath = os.path.join(RAW_DIR, 'frosh_ethnicity.csv')
    df = pd.read_csv(filepath, encoding='utf-16', sep='\t')
    df.columns = df.columns.str.strip()
    df.dropna(how='all', inplace=True)
    df.rename(columns={
        'Applicant characteristics': 'Race/ethnicity',
        'Race/ethnicity': 'Applicants'
    }, inplace=True)
    df['Applicants'] = (
        df['Applicants']
        .astype(str)
        .str.replace(',', '')
        .astype(int)
    )
    return df[['Fall term', 'Race/ethnicity', 'Applicants']]


def load_and_clean_admit_counts(filepath: str = None) -> pd.DataFrame:
    """
    Load & clean freshman admits data.
    Returns columns: ['Fall term', 'Admits']
    """
    if filepath is None:
        filepath = os.path.join(RAW_DIR, 'frosh_admit_counts.csv')
    try:
        df = pd.read_csv(filepath, encoding='utf-16', sep='\t')
    except (pd.errors.EmptyDataError, FileNotFoundError):
        return pd.DataFrame(columns=['Fall term', 'Admits'])
    df.columns = df.columns.str.strip()
    df.dropna(how='all', inplace=True)
    df.rename(columns={'Term': 'Fall term', 'Admits': 'Admits'}, inplace=True)
    df['Admits'] = (
        df['Admits']
        .astype(str)
        .str.replace(',', '')
        .fillna('0')
        .astype(int)
    )
    return df[['Fall term', 'Admits']]


def load_and_clean_app_and_admit_counts() -> pd.DataFrame:
    """
    Merge application and admit counts by Fall term; missing admits fill to 0.
    Returns columns: ['Fall term', 'Applicant characteristics', 'Applicants', 'Admits']
    """
    df_apps = load_and_clean_frosh_app_counts()
    df_adm = load_and_clean_admit_counts()
    df_merged = df_apps.merge(df_adm, on='Fall term', how='left')
    df_merged['Admits'] = df_merged['Admits'].fillna(0).astype(int)
    return df_merged
