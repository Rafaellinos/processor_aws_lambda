import json
from datetime import datetime
from uuid import uuid4
import dateutil.tz

import boto3
from botocore.client import Config


def lambda_handler(event, context):
    config = Config(connect_timeout=5, retries={'max_attempts': 2})
    print("event: ", event)
    print("context: ", context)
    dynamodb = boto3.resource('dynamodb', config=config)
    table = dynamodb.Table('my-simple-forms')
    try:
        record = {}
        if isinstance(event, dict):
            record = event
        else:
            record = event[0]
        brazil_tz = dateutil.tz.gettz('America/Sao_Paulo')
        table.put_item(
            Item={
                'id': str(uuid4()),
                'date': datetime.now(tz=brazil_tz).isoformat(),
                **(json.loads(record.get("body", {})) or {}),
            }
        )
    except Exception as e:
        print(e)
        print('Error putting item in dynamodb')
        return {
            'statusCode': 500,
            'body': json.dumps('Error putting item in dynamodb')
        }

    return {
        'statusCode': 200,
        'body': json.dumps('posted successfully')
    }


lambda_handler({"body": '{"name": "John Doe", "email": ""}'}, {})
