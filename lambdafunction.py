import json
import boto3
import time

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FloralBliss')

def lambda_handler(event, context):

    if event['operation'] == 'addPlant':
        return savePlant(event) 
    else: 
        return getPlants()

def savePlant(event):
    gmt_time = time.gmtime()
    now = time.strftime('%a, %d %b %Y %H:%M:%S', gmt_time)

    table.put_item(
        Item={
            'PlantID': event['plantID'],  
            'plantName': event['plantName'],
            'cost': event['cost'],
            'createdAt': now
        })

    return {
        'statusCode': 200,
        'body': json.dumps('Plant with PlantID: ' + event['plantID'] + ' created at ' + now)
    }

def getPlants():
    response = table.scan()
    items = response['Items']
    print(items)

    return {
        'statusCode': 200,
        'body': json.dumps(items),
        'headers': {
            'Content-Type': 'application/json',
        }
    }
