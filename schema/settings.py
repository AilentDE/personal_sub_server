from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    smtp_user: str = os.getenv('SMTP_USER')
    smtp_from: str = os.getenv('SMTP_FROM')
    smtp_code: str = os.getenv('SMTP_CODE')
    mssql_url: str = os.getenv('MSSQL_URL')
    aws_access_key_id: str = os.getenv('AWS_ACCESS_KEY_ID') #lambda_default
    aws_secret_access_key: str = os.getenv('AWS_SECRET_ACCESS_KEY') #lambda_default
    aws_session_token: str = os.getenv('AWS_SESSION_TOKEN') #lambda_default
    role_aws_key:str = os.getenv('ROLE_AWS_KEY')
    role_aws_secret:str = os.getenv('ROLE_AWS_SECRET')
    region_name: str = os.getenv('REGION_NAME')
    s3_bucket_name: str = os.getenv('S3_BUCKET_NAME')
    ses_sender: str = os.getenv('SES_SENDER')
    hmac_key:str = os.getenv('HMAC_KEY')
    allow_origins:str = os.getenv('ALLOW_ORIGINS')
    discord_client: str = os.getenv('DISCORD_CLIENT')
    discord_secret: str = os.getenv('DISCORD_SECRET')
    bot_token: str = os.getenv('BOT_TOKEN')

    # Cancel this if AWS Lambda Enviroment:
    model_config = SettingsConfigDict(env_file=".env")