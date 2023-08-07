import json
import boto3
from boto3.dynamodb.conditions import Key
date2 = '2023-07-20'
date = '2023-07-30'
def lambda_handler(event, context):
    client = boto3.resource('dynamodb')
    table = client.Table('Bill_Bryson_Data')

    response = table.get_item( # single
        Key = {
            'Date': date,
            'Time': '00:00'
        }
    )
    print(response['Item'])

    response = table.query(
        KeyConditionExpression = Key('Date').eq(date) & Key('Time').between('00:00', '24:00')
    )

    for item in response['Items']:
        print(item)


lambda_handler(None, None)