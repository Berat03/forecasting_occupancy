import pandas as pd
import json
import boto3
from boto3.dynamodb.conditions import Key
import csv
import datetime

def get_aws_data_to_csv(table_name, csv_file_path ):
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.scan(TableName=table_name)
    scanned_items = response['Items']

    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        csv_writer.writerow(['Date', 'Time', 'Total'])
        for item in scanned_items:
            date = item['Date']['S']
            time = item['Time']['S']
            total = item['Total']['S']
            total = int(total.replace(',', '')) # AWS stores like this, possible to change?

            csv_writer.writerow([date, time, total])

    print(f'saved to {csv_file_path}')


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
    df['Date'] = pd.to_datetime(df['Date'])
    # Will need to create a loop, as we have multiple within year
    # Can webscrape this as well
    holidays = pd.date_range(start='2023-07-14', end='2023-08-01', freq='D')
    terms = pd.date_range(start='2023-08-01', end='2023-08-07', freq='D')

    df['Holiday'] = df['Date'].isin(holidays)
    df['Term'] = df['Date'].isin(terms)

    df['Weekend'] = df['Datetime'].apply(lambda x: 1 if x.weekday() >= 5 else 0).astype(int)

    df.set_index('Datetime', inplace=True)
    df.drop(columns=['Date', 'Time'], inplace=True)

    agg_functions = {'Total': 'median', 'Weekend': 'max', 'Holiday': 'max', 'Term': 'max'}
    df_resample = df.resample(resample_period).agg(agg_functions).bfill()

    for i in ['Weekend', 'Holiday', 'Term']:
        df_resample[i] = df_resample[i].astype(int)

    return df_resample


#query(start_date='2023-07-20', end_date='2023-07-30', start_time="00:50", end_time="22:50")
print(pre_process(csv_data_file_path="./Data/Bill_Bryson_Data.csv", resample_period='H'))
#print(pre_process(csv_data_file_path="./Data/bbtable_data.csv", resample_period='H'))
#get_aws_data_to_csv(table_name="Bill_Bryson_Data", csv_file_path='./Data/Bill_Bryson_Data.csv')
