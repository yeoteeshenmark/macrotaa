import pandas as pd
from datetime import datetime

# Use dayfirst=True to correctly parse dates in format "31/1/14"
def read_data(file):
    # Specify date parser to enforce consistent parsing
    dateparse = lambda x: datetime.strptime(x, '%d/%m/%y')
    return pd.read_csv(file, index_col=0, parse_dates=True, 
                       date_format=dateparse, dayfirst=True)

# Choose a factor that exists in the factors CSV header.
# For example, instead of 'usd_index' (which doesn't exist),
# use 'USD - level'
factor_name = 'USD - level'

# Read the CSVs using the new parser
factors_df = read_data('factors_14-23_monthly.csv')
returns_df = read_data('SPX_14-23_monthly.csv')

# Ensure the indexes are sorted (if needed) to align dates
factors_df.sort_index(inplace=True)
returns_df.sort_index(inplace=True)

# Adjust build_macro_dashboard to merge on the index (dates)
def build_macro_dashboard(factors, returns, factor):
    # Only take the chosen factor column from factors and merge with returns
    df = pd.merge(factors[[factor]], returns, 
                  left_index=True, right_index=True, how='inner')
    # For testing, just return the merged dataframe
    return df

# Build dashboard using the new factor name
dash = build_macro_dashboard(factors_df, returns_df, factor_name)
print(dash.head())
