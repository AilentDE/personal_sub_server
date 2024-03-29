from fastapi import Request, Header, Depends
from fastapi_csrf_protect import CsrfProtect
from typing import Annotated
from utils.jwt import decode_jws
import re

allow_csrf_path = re.compile(r'/discordClusters/session/signIn/')
allow_login_path = re.compile(r'/discordClusters/csrfToken')

async def depend_csrf(request: Request, csrf_protect: CsrfProtect = Depends(), x_csrf_token: Annotated[str, Header()]=''):
    if allow_csrf_path.search(request.url.path) or allow_login_path.search(request.url.path):
        pass
    else:
        # await csrf_protect.validate_csrf(request)
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.' + x_csrf_token
        decode_jws(token)