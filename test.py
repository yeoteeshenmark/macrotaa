import pandas as pd
from datetime import datetime

def read_data(file):
    dateparse = lambda x: datetime.strptime(x, '%d/%m/%y')
    return pd.read_csv(file, index_col=0, parse_dates=True, 
                       date_format=dateparse, dayfirst=True)

# Choose a factor
factor_name = 'USD - level'

factors_df = read_data('factors_15-23_monthly.csv')
spx_df = read_data('SPX_15-23_monthly.csv')
rut_df = read_data('RUT_15-23_monthly.csv')

# Sort dataframes to align dates
factors_df.sort_index(inplace=True)
spx_df.sort_index(inplace=True)
rut_df.sort_index(inplace=True)

# Adjust function to include both SPX and RUT
def build_macro_dashboard(factors, spx, rut, factor):
    df = pd.merge(factors[[factor]], spx, left_index=True, right_index=True, how='inner')
    df = pd.merge(df, rut, left_index=True, right_index=True, how='inner', suffixes=('_SPX', '_RUT'))
    return df

# Build dashboard
dash = build_macro_dashboard(factors_df, spx_df, rut_df, factor_name)
print(dash.head())
