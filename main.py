from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from routers import email
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

handler = Mangum(app)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/return/{message}")
def read_item(message: str, q: str|None = None):
    return {"detail": message, "q": q}

@app.get('/error')
async def test_error():
    raise HTTPException(
        status_code=400,
        detail='error information.'
    )

@app.get('/setting')
async def print_setting(settings: Annotated[Settings, Depends(get_settings)]):
    return settings.model_dump()

# uvicorn main:app --reload