from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.HL import email

app = FastAPI(
    title='clusters sub-Server',
    version='0.0.1'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'DELETE'],
    allow_headers=["*"],
)

app.include_router(email.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# uvicorn main:app --reload