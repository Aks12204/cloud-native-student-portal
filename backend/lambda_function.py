import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('StudentData')

def lambda_handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,DELETE'
    }
    
    try:
        # Resolve HTTP Method across REST API & HTTP API event structures
        http_method = event.get('httpMethod')
        if not http_method and 'requestContext' in event:
            http_method = event['requestContext'].get('http', {}).get('method')
            
        # Handle Preflight OPTIONS Request
        if http_method == 'OPTIONS':
            return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'CORS OK'})}

        # 1. GET ALL STUDENTS
        elif http_method == 'GET':
            response = table.scan()
            items = response.get('Items', [])
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(items)
            }
            
        # 2. CREATE NEW STUDENT
        elif http_method == 'POST':
            body = event.get('body', {})
            if isinstance(body, str):
                body = json.loads(body) if body else {}
            
            student_id = body.get('student_id')
            name = body.get('name')
            course = body.get('course')
            email = body.get('email', 'N/A')
            
            if not student_id or not name:
                return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'Missing student_id or name'})}
            
            table.put_item(
                Item={
                    'student_id': str(student_id),
                    'name': str(name),
                    'course': str(course),
                    'email': str(email)
                }
            )
            return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Student added successfully!'})}

        # 3. DELETE STUDENT
        elif http_method == 'DELETE':
            body = event.get('body', {})
            if isinstance(body, str):
                body = json.loads(body) if body else {}
                
            student_id = body.get('student_id')
            
            if not student_id:
                return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'Missing student_id'})}
                
            table.delete_item(Key={'student_id': str(student_id)})
            return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Student deleted successfully!'})}

        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': f'Unsupported method: {http_method}'})}

    except Exception as e:
        return {'statusCode': 500, 'headers': headers, 'body': json.dumps({'error': str(e)})}