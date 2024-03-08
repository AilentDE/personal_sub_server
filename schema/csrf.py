from pydantic import BaseModel
import os

class CsrfSettings(BaseModel):
  cookie_key: str = "csrf-token"
  header_name: str = "X-CSRF-Token"
  secret_key: str = os.getenv('SECRET_KEY')
  cookie_secure: bool = True
  cookie_samesite: str = "none"
  max_age: int = 3600
  methods: set[str] = {"POST", "PUT", "DELETE"}