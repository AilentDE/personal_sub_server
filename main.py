from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.email import email

from mangum import Mangum

app = FastAPI(
    title='clusters sub-Server',
    version='0.0.1',
    docs_url='/v1/see_the_docs'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

# uvicorn main:app --reload