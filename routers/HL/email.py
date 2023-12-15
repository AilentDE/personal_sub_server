from fastapi import APIRouter, BackgroundTasks, HTTPException, Body
from typing import Annotated
import smtplib
from email.mime.text import MIMEText

router = APIRouter(
    prefix='/HL',
    tags=['HL']
)

@router.get('/test')
async def test_api():
    return {
        'success': True,
        'detail': 'hi mail.'
    }

@router.get('/error')
async def test_error():
    raise HTTPException(
        status_code=400,
        detail='error information.'
    )

# 避免未來結構變更直接用dict接收body
@router.post('/createPost')
async def when_create_work(work: Annotated[dict, Body(description='creatorPost')]):
    print(work)
    return {
        'success': True,
        'detail': work
    }