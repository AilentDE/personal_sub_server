from fastapi import FastAPI, HTTPException, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from routers import email, aws_tools
from schema.settings import Settings
from config.setting import get_settings, setting

from mangum import Mangum

app = FastAPI(
    title='clusters sub-Server',
    version='0.0.1',
    docs_url='/v1/see_the_docs'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[setting.allow_origins],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'DELETE'],
    allow_headers=["*"],
)

app.include_router(email.router)
app.include_router(aws_tools.router)

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

# uvicorn main:app --reload