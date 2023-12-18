from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    smtp_user: str
    smtp_from: str
    smtp_code: str
    mssql_url_production: str
    mssql_url_staging: str

    model_config = SettingsConfigDict(env_file=".env") #Adjust if use AWS Lambda Enviroment
    