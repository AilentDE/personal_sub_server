from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from utils.jwt import decode_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def oauth_check(token: Annotated[str, Depends(oauth2_scheme)]):
    return decode_jwt(token)