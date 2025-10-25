import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('feedback')

def lambda_handler(event, context):
    try:
        # Support API Gateway v1 and v2 style events
        # Extract body whether event['body'] exists or direct test invocation
        raw_body = None
        if isinstance(event, dict) and 'body' in event:
            raw_body = event['body']
        else:
            raw_body = event

        # If raw_body is a JSON string, parse it
        if isinstance(raw_body, str):
            body = json.loads(raw_body)
        else:
            body = raw_body or {}

        name = body.get('name')
        email = body.get('email')
        message = body.get('message')

        # simple validation
        if not name or not message:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Name and message are required'})
            }

        feedback_id = str(uuid.uuid4())

        table.put_item(Item={
            'ID': feedback_id,
            'name': name,
            'email': email,
            'message': message
        })

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'status': 'success', 'message': 'Feedback saved!'})
        }

    except Exception as e:
        print("Error:", e)
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'error': str(e)})
        }
