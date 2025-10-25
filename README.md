🌩️ Serverless Feedback

A serverless feedback submission app built using AWS Lambda, API Gateway, DynamoDB, S3, and CloudFront.
This project allows users to submit feedback through a clean, elegant web form — automatically stored in DynamoDB through an API built with Lambda.

🚀 Features

🗂️ Static Frontend hosted on Amazon S3 + distributed globally with CloudFront
⚙️ API Gateway endpoint for handling feedback submissions
🧠 AWS Lambda function that processes incoming feedback and saves to DynamoDB
🪣 DynamoDB table (feedback) to persist user feedback
🌍 Fully serverless, scalable, and cost-efficient
💌 (Optional) Email notifications using Amazon SES

🧠 Architecture Overview
[Frontend (HTML/CSS/JS)] 
       │
       ▼
[Amazon API Gateway]  --->  [AWS Lambda: submitFeedback]
       │
       ▼
[Amazon DynamoDB: feedback table]


Optional future integrations:

✅ Email notifications (via Amazon SES or EmailJS)
✅ Admin dashboard for viewing feedback

🧩 AWS Resources Used
Service	Purpose
S3	Hosts the static frontend website
CloudFront	Provides CDN distribution and HTTPS security
API Gateway	Acts as the public API endpoint
Lambda	Handles backend logic (Python)
DynamoDB	Stores feedback records

🛠️ Tech Stack

Frontend: HTML, CSS, JavaScript
Backend: Python (AWS Lambda)
Database: DynamoDB
Infrastructure: AWS S3, CloudFront, API Gateway

⚙️ Lambda Code (submit_feedback.py)
import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('feedback')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        name = body.get('name')
        email = body.get('email')
        message = body.get('message')

        feedback_id = str(uuid.uuid4())

        table.put_item(Item={
            'ID': feedback_id,
            'name': name,
            'email': email,
            'message': message
        })

        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'status': 'success', 'message': 'Feedback saved!'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }

💻 Live Demo

Frontend (CloudFront URL):
🔗 https://d3vi5nrbca9hr.cloudfront.net/

API Endpoint (API Gateway):
🔗 https://zm3yo319r2.execute-api.us-east-1.amazonaws.com


🧩 Challenges Faced

❌ “Not Found” error — fixed by creating the correct /feedback route in API Gateway.
⚠️ Case sensitivity in DynamoDB (ID vs id) caused write errors — fixed by matching key name.
🔄 Fixed CORS issues by enabling headers and redeploying API Gateway.
📁 CloudFront “NoSuchKey” error — caused by wrong S3 file path.
📬 Future Improvements
💌 Add email confirmation using Amazon SES.
📊 Create a simple admin dashboard to view stored feedback.
☁️ Deploy infrastructure automatically using Terraform or AWS CDK.

📘 Author

James Ogbodu
💼 AWS Cloud Enthusiast | Serverless Developer | Building Scalable Cloud Projects

🪪 License
This project is licensed under the MIT License
