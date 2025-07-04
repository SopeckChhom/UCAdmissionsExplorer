# scripts/clean_data
import pandas as pd

import pandas as pd

def load_and_clean_frosh_app_counts(filepath='../data/frosh_app_counts.csv'):
    df = pd.read_csv(filepath, encoding='utf-16', sep='\t')
    df.dropna(how='all', inplace=True)
    df.rename(columns={'Residency': 'Applicants'}, inplace=True)
    df['Applicants'] = df['Applicants'].str.replace(',', '').astype(int)
    return df

