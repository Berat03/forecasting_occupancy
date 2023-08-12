import matplotlib.pyplot as plt
import pandas as pd

def pre_process(csv_data_file_path, resample_period='H'):
    df = pd.read_csv(csv_data_file_path, delimiter=',')
    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%Y-%m-%d %H:%M')
    df.dropna(inplace=True)
    # Exog variables
    holidays = pd.date_range(start='2023-07-14', end='2023-07-28', freq='D')
    terms = pd.date_range(start='2023-07-29', end='2023-08-12', freq='D')
    df['Holiday'] = pd.to_datetime(df['Datetime'].dt.date).isin(holidays).astype(int)
    df['Term'] = pd.to_datetime(df['Datetime'].dt.date).isin(terms).astype(int)
    df['Weekend'] = df['Datetime'].apply(lambda x: 1 if x.weekday() >= 5 else 0).astype(int)
    df.set_index('Datetime', inplace=True)
    df.sort_index(ascending=True, inplace=True)
    df.drop(columns=['Date', 'Time'], inplace=True)
    agg_functions = {'Total': 'median', 'Weekend': 'max', 'Holiday': 'max', 'Term': 'max'} #
    df_resample = df.resample(resample_period).agg(agg_functions).bfill()

    assert (df_resample['Total'].isna().sum() == 0)
    return df_resample


df = pre_process(csv_data_file_path='./Data/Bill_Bryson_Data.csv',resample_period='H')
print(df)
df_reset = df.reset_index(drop=True)
df_reset.drop(columns=['Total'], inplace=True)
df_reset.plot()
plt.show()

