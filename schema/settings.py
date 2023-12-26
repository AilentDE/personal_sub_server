from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    smtp_user: str = os.getenv('SMTP_USER')
    smtp_from: str = os.getenv('SMTP_FROM')
    smtp_code: str = os.getenv('SMTP_CODE')
    mssql_url: str = os.getenv('MSSQL_URL')
    aws_access_key_id: str = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key: str = os.getenv('AWS_SECRET_ACCESS_KEY')
    region_name: str = os.getenv('REGION_NAME')
    s3_bucket_name: str = os.getenv('S3_BUCKET_NAME')
    ses_sender: str = os.getenv('SES_SENDER')

    # Cancel this if AWS Lambda Enviroment:
    model_config = SettingsConfigDict(env_file=".env")