from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    smtp_user: str = os.getenv('SMTP_USER')
    smtp_from: str = os.getenv('SMTP_FROM')
    smtp_code: str = os.getenv('SMTP_CODE')
    mssql_url: str = os.getenv('MSSQL_URL')

    # Cancel this if AWS Lambda Enviroment:
    model_config = SettingsConfigDict(env_file=".env")