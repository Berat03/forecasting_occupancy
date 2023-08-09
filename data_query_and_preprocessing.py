import pandas as pd
import json
import boto3
from boto3.dynamodb.conditions import Key


def query(start_date, end_date, start_time, end_time):  # Query function, to be used in website
    client = boto3.resource('dynamodb')
    table = client.Table('Bill_Bryson_Data')

    response = table.get_item(
        Key={
            'Date': start_date,
            'Time': start_time
        }
    )
    print(response['Item'])

    response = table.query(
        KeyConditionExpression=Key('Date').eq(start_date) & Key('Time').between(start_time, end_time)
    )

    for item in response['Items']:
        print(item)


def pre_process(csv_data_file_path, resample_period='H'):
    df = pd.read_csv(csv_data_file_path)
    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    # Date, Time or Datetime? Does this being separate make queries faster
    df.set_index('Datetime', inplace=True)  # as time series
    df.drop(columns=['Date', 'Time'], inplace=True)
    df_resample = df['Total'].resample(resample_period).mean().bfill()  # bfill(), direction doesn't matter?
    # Will have to add loop when I want room occupancy later
    assert (not (df_resample.isna().any()))
    return df_resample


#query(start_date='2023-07-20', end_date='2023-07-30', start_time="00:50", end_time="22:50")
#print(pre_process(csv_data_file_path="./Data/Bill_Bryson_Data.csv", resample_period='H'))
#print(pre_process(csv_data_file_path="./Data/bbtable_data.csv", resample_period='H'))
