import boto3
import csv

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb')

# Define the table name
table_name = 'YourTableName'

table_name = 'Bill_Bryson_Data'
response = dynamodb.scan(TableName=table_name)

# Retrieve the scanned items
scanned_items = response['Items']

# Define the CSV file path
csv_file_path = 'Bill_Bryson_Data_asCSV.csv'

# Write the scanned items to a CSV file
with open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write the header row
    csv_writer.writerow(['Date', 'Time', 'Total'])  # Replace 'OtherAttributes' with your actual attribute names

    # Write each item's data to the CSV file
    for item in scanned_items:
        date = item['Date']['S']
        time = item['Time']['S']
        # Replace 'OtherAttributes' with the actual attribute names you want to include in the CSV
        other_attributes = item.get('Total', {}).get('S', '')  # Replace 'OtherAttributes' with actual attribute names
        csv_writer.writerow([date, time, other_attributes])

print(f'Data saved to {csv_file_path}')
# {'Date': '2023-07-30', 'lvl4nsw': '370', 'lvl1nswe': '320', 'lvl3nsw': '420',
# 'lvl2e': '186', 'Total': '1,800', 'Time': '21:03', 'lvl4e': '200', 'lvl3e': '150'}