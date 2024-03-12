from fastapi import FastAPI, HTTPException, status, Depends, Body, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from routers import email, aws_tools
from schema.settings import Settings
from config.setting import get_settings, setting
from schema.csrf import CsrfSettings
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from fastapi.exceptions import RequestValidationError

app = FastAPI(
    title='clusters sub-Server',
    version='0.0.1',
    docs_url='/v1/see_the_docs'
)

app.add_middleware(
    CORSMiddleware,
    # allow_origins=[setting.allow_origins],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'DELETE'],
    allow_headers=["*"],
)

app.include_router(email.router)
app.include_router(aws_tools.router)

from routers.discdordClusters import session, discord, csrf
from dependencies.csrf import depend_csrf
@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()

subapi = FastAPI(dependencies=[Depends(depend_csrf)])
subapi.include_router(csrf.router)
subapi.include_router(session.router)
subapi.include_router(discord.router)
app.mount('/discordClusters', subapi)

from mangum import Mangum
handler = Mangum(app)

@app.get("/")
def test_ok():
    return {"Hello": "World"}

@app.get('/error')
async def test_error():
    raise HTTPException(
        status_code=400,
        detail='error information.'
    )

@app.post('/setting')
async def print_setting(settings: Annotated[Settings, Depends(get_settings)], check_key: Annotated[dict, Body()]):
    if check_key['hmac_key'] == settings.hmac_key:
        return settings.model_dump()
    else:
        raise HTTPException(
            status_code=400,
            detail='key fail.'
        )
    
@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

@subapi.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: Exception):
  return JSONResponse(
      status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            'message': '輸入資料不正確',
            'detail': f"{exc}"
        }
  )

@subapi.exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR)
async def internal_exception_handler(request: Request, exc: Exception):
  raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail= f"{exc}"
  )

# uvicorn main:app --reload