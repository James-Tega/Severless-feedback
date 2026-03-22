 🌩️ Serverless Feedback App

A fully serverless feedback submission app built on AWS. Users submit feedback through a clean web form — data is processed by Lambda and stored in DynamoDB, with no server required.

  Live Demo
**Frontend:** https://d3jd94tvt098le.cloudfront.net

---

Architecture

```
[Frontend: S3 + CloudFront]
        ↓
[Amazon API Gateway - POST /feedback]
        ↓
[AWS Lambda - submitFeedback (Python)]
        ↓
[Amazon DynamoDB - feedback table]
```

---

  Features

- Static frontend hosted on **Amazon S3** and distributed globally via **CloudFront**
- **HTTPS** enabled automatically through CloudFront
- **API Gateway** endpoint handles form submissions
- **AWS Lambda** (Python) processes and stores feedback
- **DynamoDB** persists every submission with a unique UUID
- Fully serverless — no EC2, no servers, near-zero cost

---

 AWS Services Used

| Service | Purpose |
|---|---|
| S3 | Hosts the static frontend |
| CloudFront | CDN distribution + HTTPS |
| API Gateway | Public HTTP endpoint (POST /feedback) |
| Lambda | Backend logic (Python) |
| DynamoDB | NoSQL database for storing feedback |

---

  Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python (AWS Lambda)
- **Database:** DynamoDB
- **Infrastructure:** AWS S3, CloudFront, API Gateway

---

⚙️ Lambda Function

```python
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
```

---

 🔄 How to Redeploy

1. **DynamoDB** — Create a table named `feedback` with partition key `ID` (String)
2. **Lambda** — Create a Python 3.12 function, paste the code above, set handler to `lambda_function.lambda_handler`, attach `AmazonDynamoDBFullAccess` policy
3. **API Gateway** — Create an HTTP API with a POST route at `/feedback` pointing to your Lambda function
4. **S3** — Create a bucket, enable static website hosting, upload `index.html`
5. **CloudFront** — Create a distribution pointing to S3, set default root object to `index.html`, disable WAF

> ⚠️ **Important:** Do NOT enable WAF or AWS Shield — these incur charges even at low traffic. For portfolio projects they are unnecessary.

---

  Lessons Learned

- **Runtime mismatch** — accidentally set Lambda runtime to Node.js instead of Python, causing `ImportModuleError`. Always verify runtime matches your code language.
- **Handler configuration** — handler must match filename and function: `lambda_function.lambda_handler`
- **File naming** — S3 default root object must exactly match the uploaded filename (`index.html`)
- **WAF costs** — WAF enabled by default on some CloudFront plans. Always explicitly disable it for portfolio/personal projects.
- **CORS** — API Gateway requires `Access-Control-Allow-Origin: *` in Lambda response headers for browser requests to work

---
  Author

**James Ogbodu** — AWS Cloud Engineer

- 💼 [LinkedIn](https://www.linkedin.com/in/james-ogbodu-18953427a) 
- 🐙 [GitHub](https://github.com/James-Tega)
