import boto3
import csv

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

get_aws_data_to_csv(table_name="Bill_Bryson_Data", csv_file_path='./Data/Bill_Bryson_Data.csv')
