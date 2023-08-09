import json
import boto3
from boto3.dynamodb.conditions import Key
start = '2023-07-20'
end = '2023-07-30'
def lambda_handler(event= None, context= None):
    client = boto3.resource('dynamodb')
    table = client.Table('Bill_Bryson_Data')

    response = table.get_item(
        Key = {
            'Date': end,
            'Time': '00:00'
        }
    )
    print(response['Item'])

    response = table.query(
        KeyConditionExpression =Key('Date').eq(end) & Key('Time').between('00:00', '24:00')
    )

    for item in response['Items']:
        print(item)

lambda_handler()