# aws.py
from decouple import config
import boto3
from botocore.exceptions import ClientError

def get_aws_credentials():
    return {
        'aws_access_key_id': config('AWS_ACCESS_KEY_ID'),
        'aws_secret_access_key': config('AWS_SECRET_ACCESS_KEY'),
        'aws_region': config('AWS_DEFAULT_REGION'),
    }

def get_ecr_client():
    credentials = get_aws_credentials()
    
    try:
        ecr = boto3.client('ecr', region_name=credentials['aws_region'], aws_access_key_id=credentials['aws_access_key_id'], aws_secret_access_key=credentials['aws_secret_access_key'])
        return ecr
    except ClientError as e:
        # Handle the exception or raise it depending on your application's needs
        raise e
