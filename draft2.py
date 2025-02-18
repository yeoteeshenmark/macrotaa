import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

def read_data(file):
    dateparse = lambda x: datetime.strptime(x, '%d/%m/%y')
    return pd.read_csv(file, index_col=0, parse_dates=True, 
                       date_format=dateparse, dayfirst=True)

# Choose a factor available in the factors CSV
factor_name = 'USD - level'

factors_df = read_data('factors_15-23_monthly.csv')
spx_df     = read_data('SPX_15-23_monthly.csv')    # Large cap (SPX)
rut_df     = read_data('RUT_15-23_monthly.csv')    # Small cap (Russell 2000)

# Sort dataframes by date to ensure alignment
factors_df.sort_index(inplace=True)
spx_df.sort_index(inplace=True)
rut_df.sort_index(inplace=True)

# Build the macro dashboard dataframe
# First, merge factors and SPX on the date index; then merge with RUT.
def build_macro_dashboard(factors, spx, rut, factor):
    # Merge factors (only the chosen factor) with SPX returns.
    df = pd.merge(factors[[factor]], spx, left_index=True, right_index=True, 
                  how='inner')
    # Merge with RUT returns. Overlapping columns get suffixed.
    df = pd.merge(df, rut, left_index=True, right_index=True, how='inner', 
                  suffixes=('_SPX', '_RUT'))
    return df

dashboard_df = build_macro_dashboard(factors_df, spx_df, rut_df, factor_name)

# In our SPX CSV sample the return column is named "Close"
# In the RUT CSV sample, the column header is "Close/Last". Due to merging,
# SPX's "Close" becomes "Close_SPX" and RUT's becomes "Close/Last_RUT".
# Rename RUT's column for clarity.
if 'Close/Last_RUT' in dashboard_df.columns:
    dashboard_df.rename(columns={'Close/Last_RUT': 'Close_RUT'}, inplace=True)

# ----- Extra analysis from draft.py -----
# Example: compute correlations between the chosen factor and the returns.
# Ensure the SPX and RUT return columns exist.
if 'Close_SPX' in dashboard_df.columns:
    corr_spx = dashboard_df[[factor_name, 'Close_SPX']].corr().iloc[0,1]
    print("Correlation between {} and SPX: {:.4f}".format(factor_name, corr_spx))
if 'Close_RUT' in dashboard_df.columns:
    corr_rut = dashboard_df[[factor_name, 'Close_RUT']].corr().iloc[0,1]
    print("Correlation between {} and RUT: {:.4f}".format(factor_name, corr_rut))

# Example: additional analysis (e.g., plotting the series)
plt.figure(figsize=(10,6))
plt.plot(dashboard_df.index, dashboard_df[factor_name], label=factor_name)
if 'Close_SPX' in dashboard_df.columns:
    plt.plot(dashboard_df.index, dashboard_df['Close_SPX'], label='SPX Close')
if 'Close_RUT' in dashboard_df.columns:
    plt.plot(dashboard_df.index, dashboard_df['Close_RUT'], label='RUT Close')
plt.title("Macro Dashboard")
plt.xlabel("Date")
plt.ylabel("Value")
plt.legend()
plt.show()

# ----- Additional draft.py analyses can be appended below -----
# For example, further regressions, rolling statistics, etc.
# (Keep all your extra analysis code here, now operating on dashboard_df)
