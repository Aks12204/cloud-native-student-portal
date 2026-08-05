import json
import logging
import boto3
from botocore.exceptions import ClientError

# Configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
TABLE_NAME = 'StudentData'
table = dynamodb.Table(TABLE_NAME)

# Standard CORS headers
CORS_HEADERS = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token',
    'Access-Control-Allow-Methods': 'OPTIONS,GET,POST,DELETE'
}

def lambda_handler(event, context):
    """
    AWS Lambda Handler for Student Portal CRUD Operations.
    Supported HTTP Methods: GET, POST, DELETE, OPTIONS
    """
    logger.info("Received event: %s", json.dumps(event))
    
    # Extract HTTP method across REST API (v1) and HTTP API (v2) payloads
    http_method = event.get('httpMethod')
    if not http_method and 'requestContext' in event:
        http_method = event['requestContext'].get('http', {}).get('method') or event['requestContext'].get('httpMethod')
    
    if not http_method:
        http_method = 'GET'
        
    http_method = http_method.upper()

    # Preflight OPTIONS request
    if http_method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': CORS_HEADERS,
            'body': json.dumps({'message': 'CORS preflight check successful'})
        }

    try:
        # ---------------------------------------------------------------------
        # 1. GET: Fetch all student records
        # ---------------------------------------------------------------------
        if http_method == 'GET':
            response = table.scan()
            items = response.get('Items', [])
            return {
                'statusCode': 200,
                'headers': CORS_HEADERS,
                'body': json.dumps(items)
            }

        # ---------------------------------------------------------------------
        # 2. POST: Add or Update a student record
        # ---------------------------------------------------------------------
        elif http_method == 'POST':
            raw_body = event.get('body', {})
            body = {}
            if isinstance(raw_body, str):
                body = json.loads(raw_body) if raw_body.strip() else {}
            elif isinstance(raw_body, dict):
                body = raw_body

            student_id = str(body.get('student_id', '')).strip()
            name = str(body.get('name', '')).strip()
            email = str(body.get('email', '')).strip()
            course = str(body.get('course', '')).strip()

            if not student_id or not name:
                return {
                    'statusCode': 400,
                    'headers': CORS_HEADERS,
                    'body': json.dumps({'error': 'Missing required fields: student_id and name are mandatory.'})
                }

            item = {
                'student_id': student_id,
                'name': name,
                'email': email if email else 'N/A',
                'course': course if course else 'General'
            }

            table.put_item(Item=item)
            logger.info("Saved student record: %s", item)

            return {
                'statusCode': 200,
                'headers': CORS_HEADERS,
                'body': json.dumps({
                    'message': 'Student record successfully saved.',
                    'student': item
                })
            }

        # ---------------------------------------------------------------------
        # 3. DELETE: Delete student record by student_id
        # ---------------------------------------------------------------------
        elif http_method == 'DELETE':
            raw_body = event.get('body', {})
            body = {}
            if isinstance(raw_body, str):
                body = json.loads(raw_body) if raw_body.strip() else {}
            elif isinstance(raw_body, dict):
                body = raw_body

            # Check query string parameters as fallback
            query_params = event.get('queryStringParameters') or {}
            student_id = body.get('student_id') or query_params.get('student_id')
            if student_id:
                student_id = str(student_id).strip()

            if not student_id:
                return {
                    'statusCode': 400,
                    'headers': CORS_HEADERS,
                    'body': json.dumps({'error': 'Missing required parameter: student_id.'})
                }

            table.delete_item(Key={'student_id': student_id})
            logger.info("Deleted student_id: %s", student_id)

            return {
                'statusCode': 200,
                'headers': CORS_HEADERS,
                'body': json.dumps({'message': f'Student ID {student_id} successfully deleted.'})
            }

        else:
            return {
                'statusCode': 405,
                'headers': CORS_HEADERS,
                'body': json.dumps({'error': f'HTTP Method {http_method} Not Allowed.'})
            }

    except ClientError as ce:
        logger.error("DynamoDB ClientError: %s", str(ce))
        return {
            'statusCode': 500,
            'headers': CORS_HEADERS,
            'body': json.dumps({'error': f'Database error: {ce.response["Error"]["Message"]}'})
        }
    except Exception as e:
        logger.error("Unhandled Exception: %s", str(e))
        return {
            'statusCode': 500,
            'headers': CORS_HEADERS,
            'body': json.dumps({'error': f'Internal Server Error: {str(e)}'})
        }