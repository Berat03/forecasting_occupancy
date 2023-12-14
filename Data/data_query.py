import pandas as pd
import json
import datetime
import boto3
from boto3.dynamodb.conditions import Key
import csv

dynamodb = boto3.resource('dynamodb')


def get_aws_data_to_csv(table_name, csv_file_path):
    table = dynamodb.Table(table_name)
    response = table.scan()

    data = response['Items']

    while 'LastEvaluatedKey' in response: # pagination of sort
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    headers = data[0].keys()
    print(headers)
    print(len(data))

    desired_fields = ['Date', 'Time', 'Total']

    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=desired_fields)
        writer.writeheader()

        for row in data:
            try: #missing data
                row['Total'] = row['Total'].replace(',', '')
            except:
                row['Total'] = None
            filtered_row = {field: row[field] for field in desired_fields}
            writer.writerow(filtered_row)

    print(f'Data written to {csv_file_path}')

    print(f'saved to {csv_file_path}')


def query(start_date, end_date, start_time, end_time, table_name):  # Query function, to be used in website
    table = dynamodb.Table(table_name)

    response = table.get_item(
        Key={
            'Date': start_date,
            'Time': start_time
        }
    )
    print(response['Item'])

    response = table.query(
        KeyConditionExpression=Key('Date').between(start_date, end_date) & Key('Time').between(start_time, end_time)
    )

    for item in response['Items']:
        print(item)

get_aws_data_to_csv('Bill_Bryson_Data', './Data/Data_AWS_141223')
