import pandas as pd
import numpy as np

# percentiles
def get_quartile(val, lower_q, upper_q):
    if val <= lower_q:
        return 'low'
    elif val >= upper_q:
        return 'high'
    else:
        return 'medium'

# is factor going up or down over t0 to t+1
def get_direction(change):
    up_min = 0.05
    down_min = -0.05
    if change >= up_min:
        return 'rising'
    elif change <= down_min:
        return 'declining'
    else:
        return 'stable'

## MAIN
def build_macro_dashboard(factors_df, returns_df, 
                          factor_name='usd_index',
                          asset_pair=('SmallCap','LargeCap'),
                          rise_thresh=0.05, drop_thresh=-0.05):
    # factors_df
        # column = factor
        # row = time
    # returns_df 
        # column = asset
        # row = % change over time
    # asset_pair: a tuple naming two columns from returns_df
    # rise_thresh, drop_thresh: scenario thresholds

    # merge data frames
    df = pd.merge(factors_df[[factor_name]], 
                  returns_df[[asset_pair[0], asset_pair[1]]],
                  left_index=True, right_index=True, how='inner')

    # get 12m forward return of assets / 12m change for factor
    df['ret_ahead_' + asset_pair[0]] = (
            df[asset_pair[0]].shift(-12) / df[asset_pair[0]] - 1
            )
    df['ret_ahead_' + asset_pair[1]] = (
            df[asset_pair[1]].shift(-12) / df[asset_pair[1]] - 1
            )
    df['factor_change'] = (
            df[factor_name].shift(-12) / df[factor_name] - 1
            )
    # drop row is no data
    df.dropna(inplace=True)

    # get low/medium/high 
    lower_q = df[factor_name].quantile(0.25)
    upper_q = df[factor_name].quantile(0.75)
    df['initial_condition'] = df[factor_name].apply(
            lambda x: get_quantile(x, lower_q, upper_q)
            )

    # get rising/declining/stable
    df['scenario'] = df['factor_change'].apply(
            lambda x: get_direction(x, rise_thresh, drop_thresh)
            )

    # get relative return between assets
    df['rel_return'] = df['ret_ahead_' + asset_pair[0]] - \
            df['ret_ahead_' + asset_pair[1]]

    # group by L/M/H and R/D/S
    group_cols = ['initial_condition', 'scenario']
    # then make new df with
        # number of entries
        # average rel. return (mean)
        # % of mean above 0
        # 10th and 90th percentiles of mean 
    summary = df.groupby(group_cols)['rel_return'].agg(
            count='count',
            avg_return='mean',
            hit_rate=lambda x: (x > 0).mean(),
            p10=lambda x: np.percentile(x,10),
            p90=lambda x: np.percentile(x,90)
            ).reset_index()

    return summary


factors_df = pd.read_csv('macro_factors.csv', index_col=0, parse_dates=True)
returns_df = pd.read_csv('asset_returns.csv', index_col=0, parse_dates=True)

dash = build_macro_dashboard(factors_df, returns_df,
                              factor_name='usd_index',
                              asset_pair=('Russell2000','Russell1000'))
print(dash)
