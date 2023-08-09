import pandas as pd


def pre_process(csv_data_file_path, resample_period='H'):
    df = pd.read_csv(csv_data_file_path)
    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    # Date, Time or Datetime? Does this being separate make queries faster
    df.set_index('Datetime', inplace=True)  # as time series
    df.drop(columns=['Date', 'Time'], inplace=True)
    df_resample = df['Total'].resample(resample_period).mean().bfill()  # bfill(), direction doesn't matter?
    # Will have to add loop when I want room occupancy later
    assert (not(df_resample.isna().any()))
    return df_resample

print(pre_process(csv_data_file_path="./Data/Bill_Bryson_Data.csv", resample_period='H'))
print(pre_process(csv_data_file_path="./Data/bbtable_data.csv", resample_period='H'))

