import pandas as pd
import json
import boto3
from boto3.dynamodb.conditions import Key
import csv
import datetime


def get_aws_data_to_csv(table_name, csv_file_path):
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
            total = int(total.replace(',', ''))  # AWS stores like this, possible to change?

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

# query(start_date='2023-07-20', end_date='2023-07-30', start_time="00:50", end_time="22:50")
# get_aws_data_to_csv(table_name="Bill_Bryson_Data", csv_file_path='./Data/Bill_Bryson_Data.csv')
