from fastapi import HTTPException, status, Depends, Header
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from utils.jwt import decode_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/session/discord")

def oauth_check(token: Annotated[str, Depends(oauth2_scheme)]):
    return decode_jwt(token)

# def oauth_check(x_authorization: Annotated[str, Header(..., description='SwaggerUI僅支援完整Oauth2輸入，這個header作為暫時取代自動oauth驗證。\n正式啟用時改回Oauth。')]):
#     scheme, param = x_authorization.split()
#     if scheme.lower() != 'bearer':
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail='Authorization ERROR.'
#         )
#     return decode_jwt(param)