import pandas as pd
import json
from datetime import datetime, timedelta
import boto3
from boto3.dynamodb.conditions import Key, Attr
import csv
import pytz

## Constants
dynamodb = boto3.resource('dynamodb')
table_name = 'Bill_Bryson_Data'
table = dynamodb.Table(table_name)

###

def get_aws_data_to_csv(csv_file_path: str) -> None:
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


def query_specific_period(start_date, end_date, start_time, end_time):  # Query function, to be used in website
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


def get_last_x_time(hours: int = 24) -> pd.DataFrame:
    curr_datetime = datetime.now().astimezone(pytz.timezone('Europe/London'))
    start_datetime = curr_datetime - timedelta(hours=hours)
    curr_date = curr_datetime.strftime('%Y-%m-%d')
    end_date = start_datetime.strftime('%Y-%m-%d')

    # Filter items based on time in-memory

    response_end = table.query(
        KeyConditionExpression=Key('Date').eq(end_date)
    )
    response_curr = table.query(
        KeyConditionExpression=Key('Date').eq(curr_date)
    )

    response = {'Items': []}
    response['Items'].extend(response_end['Items'])
    response['Items'].extend(response_curr['Items'])

    df = pd.DataFrame(response['Items'])
    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    df.set_index('Datetime', inplace=True)
    df.drop(['Date', 'Time'], axis=1, inplace=True)

    return df

get_last_x_time()

