from config.aws_boto3 import boto3Client
from botocore.exceptions import ClientError
import logging

def create_presigned_url(bucket_name:str, object_name:str, expiration:int = 3600, for_download:bool = False) -> str|None:
    """Generate a presigned URL to share an S3 object

    :param expiration: Time in seconds for the presigned URL to remain valid
    :param for_download: Use attachment header or not
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    session = boto3Client('s3')
    try:
        if for_download:
            Params={
                'Bucket': bucket_name,
                'Key': object_name,
                'ResponseContentDisposition': f"attachment; filename = file.jpg"
            }
        else:
            Params={
                'Bucket': bucket_name,
                'Key': object_name
            }
        response = session.generate_presigned_url('get_object',
                                                    Params,
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response